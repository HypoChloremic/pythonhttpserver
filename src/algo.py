
from typing import Dict, Tuple, List
import pdb

def split_box(data: Dict[str, int]):
    max_el = max(data, key=data.get)
    min_el = min(data, key=data.get)
    rest = data[max_el] % data[min_el]
    if rest > 0:
        print(f"data: {data} max {max_el} min {min_el} rest {rest}")
        return split_box(
            {
                max_el: rest,
                min_el: data[min_el]
            }
        )
    else:
        print(data)
        return data

def split_loop(data: List[int]):
    while True:
        try:
            if data[0] > data[1]:
                rest = data[0] % data[1]
                data[0] = rest
                yield data
            else:
                rest = data[1] % data[0]
                data[1] = rest
                yield data
        except ZeroDivisionError as e:
            break



if __name__ == "__main__":
    # split_box({"x": 64, "y": 168})
    gen = split_loop([64, 168])
