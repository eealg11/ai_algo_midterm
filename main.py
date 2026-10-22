import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # GAS 및 웹 클라이언트와의 통신을 위한 CORS 허용

# 고정 길이 큐 클래스 정의
class FixedSizeQueue:
    def __init__(self, capacity=5):
        self.capacity = int(capacity)
        self.queue = [None] * self.capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def initialize(self, capacity=5):
        """1. 초기화"""
        self.capacity = int(capacity)
        self.queue = [None] * self.capacity
        self.front = 0
        self.rear = -1
        self.size = 0
        return f"큐가 용량 {self.capacity}로 초기화되었습니다."

    def push(self, item):
        """2. push (Enqueue)"""
        if self.is_full():
            raise OverflowError("큐가 가득 찼습니다 (Overflow).")
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self.size += 1
        return item

    def pop(self):
        """2. pop (Dequeue)"""
        if self.is_empty():
            raise IndexError("큐가 비어 있습니다 (Underflow).")
        item = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item

    def get_size(self):
        """3, 8. 현재 데이터 개수(길이/크기) 반환"""
        return self.size

    def check_status(self):
        """4. 상태 검사 (full/empty)"""
        return {"is_full": self.is_full(), "is_empty": self.is_empty()}

    def peek_front(self):
        """5. 전면(Front) 데이터 확인"""
        if self.is_empty():
            return None
        return self.queue[self.front]

    def clear(self):
        """6. 큐 전체 데이터 삭제"""
        for i in range(self.capacity):
            self.queue[i] = None
        self.front = 0
        self.rear = -1
        self.size = 0
        return "큐가 전체 삭제되었습니다."

    def search_index(self, item):
        """7. 값의 index 검색 (큐 내부 논리적 순서 기준)"""
        for i in range(self.size):
            idx = (self.front + i) % self.capacity
            if self.queue[idx] == item:
                return i  # Front로부터의 상대적 위치 반환
        return -1

    def contains(self, item):
        """9. 값의 존재 여부 검사"""
        return self.search_index(item) != -1

    def print_queue(self):
        """10. Front부터 Rear 까지 출력"""
        result = []
        for i in range(self.size):
            idx = (self.front + i) % self.capacity
            result.append(self.queue[idx])
        return result

# 기본 큐 인스턴스 생성 (기본 용량: 5)
q = FixedSizeQueue(5)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Cloud Run Fixed-Size Queue Server is running!"})

@app.route("/queue", methods=["POST"])
def handle_queue():
    data = request.json or {}
    action = data.get("action")
    value = data.get("value")
    capacity = data.get("capacity", 5)

    try:
        if action == "init":
            msg = q.initialize(capacity)
        elif action == "push":
            if value is None:
                return jsonify({"error": "추가할 값이 없습니다."}), 400
            q.push(value)
            msg = f"'{value}' 푸시 성공"
        elif action == "pop":
            popped = q.pop()
            msg = f"'{popped}' 팝 성공"
        elif action == "size":
            msg = q.get_size()
        elif action == "status":
            msg = q.check_status()
        elif action == "front":
            msg = q.peek_front()
        elif action == "clear":
            msg = q.clear()
        elif action == "search":
            msg = q.search_index(value)
        elif action == "contains":
            msg = q.contains(value)
        elif action == "print":
            msg = q.print_queue()
        else:
            return jsonify({"error": "지원하지 않는 액션입니다."}), 400

        return jsonify({
            "success": True,
            "message": msg,
            "queue_state": q.print_queue(),
            "front": q.front,
            "rear": q.rear,
            "size": q.size,
            "capacity": q.capacity,
            "status": q.check_status()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
