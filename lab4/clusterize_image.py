import numpy as np
from PIL import Image


def main():
    img = Image.open('./data/rgb.gif')
    arr = np.array(img)
    print(arr)
    arr = arr.flatten(order='a')
    print(arr)


if __name__ == '__main__':
    main()
