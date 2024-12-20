class MaxHeap:
    def __init__(self):
        # Initialize empty heap for priority-based waitlist
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, key):
        # Insert new priority-user tuple and maintain heap property
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        # Bubble up element to maintain max heap property
        while i > 0 and self._compare(self.heap[self.parent(i)], self.heap[i]) < 0:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def _compare(self, a, b):
        # Compare tuples by priority first, then timestamp
        priority_a, user_id_a, timestamp_a = a
        priority_b, user_id_b, timestamp_b = b
        
        # First compare by priority (higher priority first)
        if priority_a != priority_b:
            return priority_a - priority_b
        
        # If priorities are equal, compare by timestamp
        return timestamp_b - timestamp_a  # Earlier timestamp gets priority

    def pop(self):
        # Remove and return highest priority element
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return max_val

    def _heapify_down(self, i):
        # Bubble down element to maintain max heap property
        largest = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self._compare(self.heap[left], self.heap[largest]) > 0:
            largest = left
        
        if right < len(self.heap) and self._compare(self.heap[right], self.heap[largest]) > 0:
            largest = right

        if largest != i:
            self.swap(i, largest)
            self._heapify_down(largest)

    def remove(self, user_id):
        # Remove specific user from waitlist
        for i, (_, uid, _) in enumerate(self.heap):
            if uid == user_id:
                self.swap(i, len(self.heap) - 1)
                self.heap.pop()
                if i < len(self.heap):
                    self._heapify_up(i)
                    self._heapify_down(i)
                return True
        return False

    def update_priority(self, user_id, new_priority):
        # Update priority of specific user and maintain heap property
        for i, (_, uid, timestamp) in enumerate(self.heap):
            if uid == user_id:
                self.heap[i] = (new_priority, uid, timestamp)
                self._heapify_up(i)
                self._heapify_down(i)
                return True
        return False

    def contains(self, user_id):
        # Check if user exists in waitlist
        return any(uid == user_id for _, uid, _ in self.heap)

    def get_size(self):
        # Get number of users in waitlist
        return len(self.heap)