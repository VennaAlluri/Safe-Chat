def previous_smallest_element(arr):
    stack = []
    result = []

    for num in arr:
        while stack and stack[-1] <= num:
            stack.pop()
        if not stack:
            result.append(-1)
        else:
            result.append(stack[-1])
        stack.append(num)

    return result

# Example usage:
arr = [-1, 1, 1, 10, 1,2,45]
print("Previous smallest elements:", previous_smallest_element(arr))