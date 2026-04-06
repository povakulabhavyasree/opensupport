# environment.py
# Multi-turn RL-style environment with conversation history
# Supports reset(), step(), and state() functions

from tasks import tasks, get_followup
from grader import grade_response


class Env:
    """
    A multi-turn OpenEnv-style environment for customer support.

    Features:
      - Multi-turn conversations with history tracking
      - Cumulative reward across turns
      - Detailed state() function for transparency
      - Intelligent early-exit detection

    Usage:
        env = Env()
        obs = env.reset("easy")
        obs, reward, done, info = env.step("Your reply")
        full_state = env.state()
    """

    def __init__(self):
        self.current_task = None
        self.current_task_key = None
        self.done = False
        self.turn = 0
        self.max_turns = 1
        self.history = []         # Full conversation history
        self.rewards = []         # Reward for each turn
        self.breakdowns = []      # Detailed scoring for each turn
        self.total_reward = 0.0   # Cumulative reward

    def reset(self, task_name):
        """
        Resets the environment with the given task.
        """
        if task_name not in tasks:
            raise ValueError(f"Task '{task_name}' not found in tasks.py")

        self.current_task = tasks[task_name]
        self.current_task_key = task_name
        self.done = False
        self.turn = 0
        self.max_turns = self.current_task.get("max_turns", 3)
        self.history = []
        self.rewards = []
        self.breakdowns = []
        self.total_reward = 0.0

        # Add customer's first message to history
        customer_msg = self.current_task["customer_message"]
        self.history.append({"role": "customer", "content": customer_msg})

        return customer_msg

    def step(self, action):
        """
        Takes the agent's response and returns results.
        """
        if self.done:
            return "Environment is done", 0.0, True, self.state()

        self.turn += 1

        # Add agent's response to history
        self.history.append({"role": "agent", "content": action})

        # Grade this response
        reward, breakdown = grade_response(self.current_task, action)
        self.rewards.append(reward)
        self.breakdowns.append(breakdown)
        self.total_reward += reward

        # Calculate average for early exit logic
        avg_reward = round(sum(self.rewards) / len(self.rewards), 2)

        # Check for early exit signals in agent's message
        agent_exit_signals = ["goodbye", "have a great day", "pleasure assisting", "anything else I can help"]
        bot_is_closing = any(sig in action.lower() for sig in agent_exit_signals)

        # Build observation (next message or feedback)
        followup = get_followup(self.current_task_key, self.turn + 1)
        
        # Termination logic:
        # 1. Max turns reached
        # 2. Excellent performance (early resolve)
        # 3. Agent is closing the conversation politely
        # 4. No more follow-up messages defined
        
        at_max_turns = self.turn >= self.max_turns
        high_performance = avg_reward >= 0.8 and self.turn >= 2
        
        if at_max_turns or bot_is_closing or not followup:
            self.done = True
        elif high_performance:
            # Maybe the customer has one last quick thing? 
            # If no followup, they are satisfied.
            if not followup:
                self.done = True

        if not self.done and followup:
            # Continue conversation with follow-up
            self.history.append({"role": "customer", "content": followup})
            observation = followup
        else:
            # Conversation complete — give final feedback based on average reward
            self.done = True
            if avg_reward >= 0.8:
                observation = "RESOLVED: Customer is highly satisfied. Issue handled perfectly."
            elif avg_reward >= 0.6:
                observation = "PARTIALLY RESOLVED: Good effort, but some details were missing."
            else:
                observation = "UNRESOLVED: Poor handling. Customer is unhappy."

        # Build detailed info
        info = {
            "step": self.turn,
            "reward": reward,
            "avg_reward": avg_reward,
            "total_reward": round(self.total_reward, 2),
            "done": self.done,
            "breakdown": breakdown,
        }

        return observation, reward, self.done, info

    def state(self):
        """
        Returns the full conversation state.
        """
        avg_reward = 0.0
        if self.rewards:
            avg_reward = round(sum(self.rewards) / len(self.rewards), 2)

        return {
            "task_name": self.current_task["name"] if self.current_task else None,
            "task_type": self.current_task["issue_type"] if self.current_task else None,
            "customer_mood": self.current_task["mood"] if self.current_task else None,
            "turn": self.turn,
            "max_turns": self.max_turns,
            "is_done": self.done,
            "conversation_history": self.history.copy(),
            "reward_history": self.rewards.copy(),
            "total_cumulative_reward": round(self.total_reward, 2),
            "average_reward": avg_reward,
            "detailed_breakdowns": self.breakdowns.copy(),
            "context_provided": self.current_task.get("context", {}) if self.current_task else {}
        }
