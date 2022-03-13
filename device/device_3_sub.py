import device.sub_device

CODE = 10003

if __name__ == '__main__':
    device.sub_device.run([f'CMD_{CODE}'], f'client_sub_{CODE}')