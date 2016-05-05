def my_function(rect1, rect2):
    # write the body of your function here
    x_overlap = find_x_overlap(rect1, rect2)
    if x_overlap is None:
        return None
    print x_overlap
    y_overlap = find_y_overlap(rect1, rect2)
    if y_overlap is None:
        return None
    print y_overlap
    rectangle_overlap = {

        'left_x':0,
        'bottom_y':0,
        'width':0,
        'height':0

    }
    rectangle_overlap['left_x'] = x_overlap[0]
    rectangle_overlap['bottom_y'] = y_overlap[0]
    rectangle_overlap['width'] = x_overlap[1] - x_overlap[0]
    rectangle_overlap['height'] = y_overlap[1] - y_overlap[0]
    return rectangle_overlap

def find_x_overlap(rect1, rect2):
    if rect1['left_x'] < rect2['left_x']:
        if rect1['left_x'] + rect1['width'] > rect2['left_x']:
            if rect1['left_x'] + rect1['width'] >= rect2['left_x'] + rect2['width']:
                return (rect2['left_x'], rect2['left_x'] + rect2['width'])
            else:
                return (rect2['left_x'], rect1['left_x'] + rect1['width'])
        else:
            return None
    elif rect2['left_x'] < rect1['left_x']:
        if rect2['left_x'] + rect2['width'] > rect1['left_x']:
            if rect1['left_x'] + rect1['width'] >= rect2['left_x'] + rect2['width']:
                return (rect1['left_x'], rect2['left_x'] + rect2['width'])
            else:
                return (rect1['left_x'], rect1['left_x'] + rect1['width'])
        else:
            return None
    else:
        if rect1['width'] >= rect2['width']:
            return (rect1['left_x'], rect1['left_x'] + rect2['width'])
        else:
            return (rect1['left_x'], rect1['left_x'] + rect1['width'])

def find_y_overlap(rect1, rect2):
    if rect1['bottom_y'] < rect2['bottom_y']:
        if rect1['bottom_y'] + rect1['height'] > rect2['bottom_y']:
            if rect1['bottom_y'] + rect1['height'] >= rect2['bottom_y'] + rect2['height']:
                return (rect2['bottom_y'], rect2['bottom_y'] + rect2['height'])
            else:
                return (rect2['bottom_y'], rect1['bottom_y'] + rect1['height'])
        else:
            return None
    elif rect2['bottom_y'] < rect1['bottom_y']:
        if rect2['bottom_y'] + rect2['height'] > rect1['bottom_y']:
            if rect1['bottom_y'] + rect1['height'] >= rect2['bottom_y'] + rect2['height']:
                return (rect1['bottom_y'], rect2['bottom_y'] + rect2['height'])
            else:
                return (rect1['bottom_y'], rect1['bottom_y'] + rect1['height'])
        else:
            return None
    else:
        if rect1['height'] >= rect2['height']:
            return (rect1['bottom_y'], rect1['bottom_y'] + rect2['height'])
        else:
            return (rect1['bottom_y'], rect1['bottom_y'] + rect1['height'])

# run your function through some test cases here
# remember: debugging is half the battle!
my_rectangle = {

    # coordinates of bottom-left corner
    'left_x': 3,
    'bottom_y': 6,

    # width and height
    'width': 1,
    'height': 1,

}
my_rectangle2 = {

    # coordinates of bottom-left corner
    'left_x': 2,
    'bottom_y': 5,

    # width and height
    'width': 4,
    'height': 4,

}
print my_function(my_rectangle, my_rectangle2)
