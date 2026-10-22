import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# GAS 및 프론트엔드 연동을 위한 CORS 허용
CORS(app)


class FixedSizeQueue:
  """최대 크기가 고정된 큐(Fixed-Size Queue) 클래스.

  크기가 가득 차면 가장 오래된 항목(FIFO)이 제거되고 새 항목이 추가됩니다.
  """

  def __init__(self, capacity: int = 5):
    self.capacity = capacity
    self.queue = []

  def enqueue(self, item):
    """큐에 데이터를 삽입합니다.

    용량이 가득 찬 경우 가장 먼저 들어온 데이터를 제거(Overflow 처리)합니다.
    """
    status_msg = ""
    if len(self.queue) >= self.capacity:
      removed = self.queue.pop(0)
      status_msg = f"큐 용량({self.capacity}) 초과로 가장 오래된 항목 '{removed}'이(가) 제거되었습니다."
    else:
      status_msg = f"항목 '{item}'이(가) 큐에 정상적으로 추가되었습니다."

    self.queue.append(item)
    return status_msg

  def get_state(self):
    """현재 큐의 상태와 복잡도 정보를 반환합니다."""
    return {
        "queue": list(self.queue),
        "capacity": self.capacity,
        "size": len(self.queue),
        "is_full": len(self.queue) >= self.capacity,
        # 시간 복잡도: 삽입 O(N) [파이썬 리스트 pop(0) 기준], 조회 O(1)
        # 공간 복잡도: O(Capacity)
        "complexity": {
            "time_enqueue": "O(N) (리스트 앞단 삭제 시 이동 발생)",
            "time_peek_or_view": "O(1)",
            "space": f"O({self.capacity}) (고정 크기 제한)",
        },
    }


# 기본 용량이 5인 고정 길이 큐 인스턴스 생성
fixed_queue = FixedSizeQueue(capacity=5)


@app.route("/", methods=["GET"])
def health_check():
  """서버 상태 확인용 엔드포인트"""
  return jsonify({
      "status": "healthy",
      "message": "고정 길이 큐 클라우드 런 서버가 정상 작동 중입니다.",
  })


@app.route("/queue", methods=["GET"])
def get_queue():
  """현재 고정 길이 큐의 상태 및 복잡도를 조회합니다."""
  return jsonify(fixed_queue.get_state())


@app.route("/queue", methods=["POST"])
def enqueue_item():
  """고정 길이 큐에 새로운 데이터를 추가합니다."""
  data = request.get_json() or {}
  item = data.get("item")

  if not item:
    return jsonify({"error": "추가할 항목('item')이 제공되지 않았습니다."}), 400

  action_msg = fixed_queue.enqueue(item)
  response_data = fixed_queue.get_state()
  response_data["action_message"] = action_msg

  return jsonify(response_data)


if __name__ == "__main__":
  # Cloud Run 환경 변수 PORT를 지원하며, 기본값은 8080입니다.
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)
