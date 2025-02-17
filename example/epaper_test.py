from machine import Pin, SPI
import framebuf
import utime
import gc  # 메모리 관리

class SSD1680:
    def __init__(self):
        gc.collect()  # 메모리 정리
        print("Free memory:", gc.mem_free())  # 사용 가능한 메모리 확인
        
        # SPI1 설정 (SCK=GP10, MOSI=GP11, CS=GP9)
        self.spi = SPI(1, baudrate=2000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11))
        self.cs = Pin(9, Pin.OUT)
        self.dc = Pin(8, Pin.OUT)
        self.rst = Pin(7, Pin.OUT)
        self.busy = Pin(6, Pin.IN)

        self.width = 250  
        self.height = 122

        # 작은 버퍼 사용 (부분 업데이트)
        buffer_size = (50 * 50) // 8  # 50x50 픽셀 버퍼 (312 바이트)
        self.buffer = bytearray(buffer_size)
        self.fb = framebuf.FrameBuffer(self.buffer, 50, 50, framebuf.MONO_HMSB)

        self.init_display()

    def send_command(self, command):
        """ 명령어 전송 """
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([command]))
        self.cs.value(1)

    def send_data(self, data):
        """ 데이터 전송 """
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(bytearray([data]))
        self.cs.value(1)

    def wait_until_idle(self):
        """ ePaper가 준비될 때까지 대기 """
        while self.busy.value() == 1:
            utime.sleep_ms(10)

    def reset(self):
        """ ePaper 하드웨어 리셋 """
        self.rst.value(0)
        utime.sleep_ms(10)
        self.rst.value(1)
        utime.sleep_ms(10)

    def init_display(self):
        """ ePaper 초기화 """
        self.reset()
        self.send_command(0x12)  # 소프트웨어 리셋
        self.wait_until_idle()

    def clear(self):
        """ 화면을 흰색으로 지우기 """
        self.fb.fill(1)  
        self.update_partial(0, 0)  # 부분 업데이트

    def update_partial(self, x, y):
        """ 부분 업데이트 (50x50 영역만 갱신) """
        self.send_command(0x24)  # 메모리 쓰기 모드

        for byte in self.buffer:
            self.send_data(byte)

        self.send_command(0x22)  # 화면 갱신 명령어
        self.send_data(0xF7)
        self.send_command(0x20)  # 실행
        self.wait_until_idle()

    def draw_text(self, text, x, y):
        """ 특정 위치에 텍스트 표시 """
        self.fb.fill(1)  # 배경을 흰색으로 설정
        self.fb.text(text, 5, 5, 0)  # (5,5) 위치에 표시
        self.update_partial(x, y)

# 실행 코드
epd = SSD1680()
epd.clear()
epd.draw_text("Hello, SPI1!", 20, 50)
