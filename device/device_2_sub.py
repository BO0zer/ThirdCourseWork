import device.sub_device

CODE = 10002

if __name__ == '__main__':
    directory = "configs/device_2"
    device.sub_device.run([f'CMD_{CODE}'], f'client_sub_{CODE}', directory)