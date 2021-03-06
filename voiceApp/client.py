import socket
import select
import errno
import pyaudio
import wave
import pickle
import random
import datetime
import sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
# recv() not to block
client_socket.setblocking(False)

username = bytes(my_username, "utf-8")
username_header = bytes(f"{len(username):<{HEADER_LENGTH}}", "utf-8")
client_socket.send(username_header+username)

chunk = 1024 #Record Chunks of 1024 samples
sample_format = pyaudio.paInt16 #16bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3

def record():
    # Create an interface to PortAudio
    p = pyaudio.PyAudio() 
    stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    return frames


while True:
    message = input(f"{my_username}: Type anything to start recording > ")

    # Message not empty
    if message:
        print('Recording')
        frames = record()
        print('Finished recording')
        voice_note = pickle.dumps(frames)
        message_header = bytes(f"{len(voice_note):<{HEADER_LENGTH}}", "utf-8")+voice_note
        client_socket.send(message_header)

    try:    
        # Loop over received messages
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            p = pyaudio.PyAudio() 

            if not len(username_header):
                print('Connection closed by server')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            voice_note_header = client_socket.recv(HEADER_LENGTH)
            voice_note_length = int(voice_note_header.decode('utf-8'))
            frames = []

            voicem = client_socket.recv(voice_note_length)[HEADER_LENGTH:]
            
            # voicem = pickle.loads(voicem)
            frames.append(voicem)
            timestring1 = str(datetime.datetime.now())
            # Remove unwanted characters 
            timestring2 = timestring1.replace("-", "")
            timestring3 = timestring2.replace(":", "")
            timestring4 = timestring3.replace(".", "")
            timestring = timestring4.replace(" ", "")
            timestring = f'{timestring}.wav'

            wf = wave.open(timestring, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()

            # Add autoplay functionality

            print(f'New Voice Note: {timestring} from : {username}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        #we haven't received anything
        continue

    except Exception as e:
        print('Reading error: {}'.format(str(e)))
        sys.exit()