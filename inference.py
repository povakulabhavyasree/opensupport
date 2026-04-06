# inference.py
import os
import sys

from openai import OpenAI
from environment import Env

MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

SYSTEM_PROMPT = """You are a professional e-commerce customer support agent.

Rules:
- Always give a COMPLETE solution
- Be polite, confident, and clear
- Resolve the issue in ONE response if possible
- Use strong action words like "will process", "will resolve immediately"

Handle scenarios like:
- Order tracking
- Refunds & returns
- Damaged products
- Late delivery complaints

Special instructions:
- Always mention order details
- For refunds → explain clearly
- For delays → apologize + offer solution
- For angry users → show empathy + immediate resolution

Keep response under 100 words.

Customer message:
{observation}

Now give the best possible response:
"""


def get_ai_response(client, history, context):
    messages = [{"role": "system", "content": f"{SYSTEM_PROMPT}\n\nContext: {context}"}]

    for entry in history:
        role = "assistant" if entry["role"] == "agent" else "user"
        messages.append({"role": role, "content": entry["content"]})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.4,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"


def main():
    if not os.getenv("HF_TOKEN"):
        print("ERROR: HF_TOKEN not set", file=sys.stderr)
        return

    client = OpenAI(
        base_url=os.getenv("API_BASE_URL", "https://router.huggingface.co/v1"),
        api_key=os.getenv("HF_TOKEN"),
    )

    env = Env()
    task_keys = ["easy", "medium", "hard"]

    for key in task_keys:
        env.reset(key)
        state = env.state()
        task_name = state["task_name"]

        print(f"[START] task={task_name} env=callcenter model={MODEL_NAME}")

        step_count = 0
        max_steps = 1

        while not env.done and step_count < max_steps:
            step_count += 1

            ai_reply = get_ai_response(
                client,
                state["conversation_history"],
                state["context_provided"]
            )

            if "ERROR" in ai_reply:
                print(f"[STEP] step={step_count} action=ERROR reward=0.00 done=true error={ai_reply}")
                break

            observation, reward, done, _ = env.step(ai_reply)
            state = env.state()

            clean_reply = ai_reply.replace("\n", " ").strip()
            done_str = "true" if done else "false"

            print(f"[STEP] step={step_count} action={clean_reply} reward={reward:.2f} done={done_str} error=null")

        # ✅ ALWAYS PRINT END AFTER LOOP
        state = env.state()
        final_score = state["average_reward"]
        success = final_score >= 0.7
        success_str = "true" if success else "false"

        rewards_str = ",".join([f"{r:.2f}" for r in state["reward_history"]])

        print(f"[END] success={success_str} steps={step_count} rewards={rewards_str}")


if __name__ == "__main__":
    main()