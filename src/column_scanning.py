
def column_scanning:
    #Finger detection
    finger_size_min = 15
    finger_size_max = 35
    finger_search_col_min = 0
    finger_search_col_min = 512
    hand_test_image_mask = hand_test_image_mask[300:650, 150:500]
    rows,cols = hand_test_image_mask.shape
    fingers = 0
    for i in range(rows):
        for j in range(cols):
            if hand_test_image_mask[i,j] == 255:
                if np.all(hand_test_image_mask[i:i+finger_size_min,j]==255) and hand_test_image_mask[i+finger_size_max+1,j] == 0 and hand_test_image_mask[i-finger_size_max-1,j] == 0:
                    hand_test_image_mask[i,j] = 128
                    print("finger detected")
                
    print(fingers)
