def longest_consecutive_sequence(nums):
    if not nums:
        return []

    num_set = set(nums)
    longest_seq = []

    for num in num_set:
        if num - 1 not in num_set:  # Start of a new sequence
            current_seq = []
            while num in num_set:
                current_seq.append(num)
                num += 1
            if len(current_seq) > len(longest_seq):
                longest_seq = current_seq

    return longest_seq

