import bluetooth
import jm_network
from micropython import const

# BLE 설정 값
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)  # GATT 쓰기 이벤트

# BLE 서비스 및 캐릭터리스틱 UUID
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")  # RX (수신)
_UART_TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")  # TX (전송)

_UART_SERVICE = (
    _UART_SERVICE_UUID,
    ((_UART_TX_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY),
     (_UART_RX_UUID, bluetooth.FLAG_WRITE),),
)

MY_MSG = None

class BLEUART:
    def __init__(self, name="PicoW-BLE"):
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._irq)
        self.rx_buffer = b""
        self.ssid = ""
        self.pwd = ""
        self.network_connected = False

        # GATT 서비스 등록
        ((self.tx_handle, self.rx_handle),) = self.ble.gatts_register_services([_UART_SERVICE])

        self._connections = set()
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("Central connected")
            self._connections.add(conn_handle)

        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Central disconnected")
            self._connections.remove(conn_handle)
            self._advertise()  # 연결이 끊기면 다시 광고 시작

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if value_handle == self.rx_handle:
                msg = self.ble.gatts_read(self.rx_handle).decode().strip()

                if msg[0] == '[':
                    self.rx_buffer = msg[1:]
                elif msg[-1] == ']':
                    self.rx_buffer += msg[:-1]
                    print(self.rx_buffer)

                    tkns = self.rx_buffer.split(':')
                    self.ssid = tkns[0]
                    self.pwd = tkns[1]

                    print(f"ssid: {self.ssid}")
                    print(f"pwd: {self.pwd}")

                    self.network_connected = jm_network.connect_to_wlan(self.ssid, self.pwd)
                    print(self.network_connected)
                else:
                    self.rx_buffer += msg



    def send(self, message):
        """ 스마트폰으로 메시지 전송 """
        if not self._connections:
            print("No BLE connection")
            return

        print(f"Sending: {message}")
        msg = message.encode()
        for conn_handle in self._connections:
            self.ble.gatts_notify(conn_handle, self.tx_handle, msg)

    def _advertise(self, interval_us=100000):
        adv_data = bytes([0x02, 0x01, 0x06, len("PicoW-BLE") + 1, 0x09]) + bytes("PicoW-BLE", "utf-8")
        print("Advertising BLE as:", "PicoW-BLE")
        self.ble.gap_advertise(interval_us, adv_data)