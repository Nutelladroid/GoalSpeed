import time
import numpy as np
from rlbot.agents.base_script import BaseScript
from rlbot.utils.structures.game_data_struct import GameTickPacket

class GoalSpeed(BaseScript):
    def __init__(self):
        super().__init__("Goal Speed")
        self.blue_score = 0
        self.orange_score = 0
        self.ball_speed_at_goal = 0.0
        self.display_time = 5  # seconds
        self.display_start_time = 0

    def start(self):
        while True:
            packet = self.wait_game_tick_packet()

            if self.detect_goal_scored(packet):
                self.display_start_time = time.time()
                self.render_ball_speed()

            if time.time() - self.display_start_time > self.display_time:
                self.clear_text()

    def detect_goal_scored(self, packet: GameTickPacket) -> bool:
        new_blue_score = packet.teams[0].score
        new_orange_score = packet.teams[1].score
        if new_blue_score > self.blue_score or new_orange_score > self.orange_score:
            self.blue_score = new_blue_score
            self.orange_score = new_orange_score
            self.ball_speed_at_goal = self.calculate_ball_speed(packet)
            return True
        return False

    def calculate_ball_speed(self, packet: GameTickPacket) -> float:
        ball_velocity = packet.game_ball.physics.velocity
        ball_speed = np.linalg.norm([ball_velocity.x, ball_velocity.y, ball_velocity.z])
        return ball_speed * 0.036  # Convert to km/h

    def render_ball_speed(self):
        self.game_interface.renderer.begin_rendering()
        self.game_interface.renderer.draw_string_2d(20, 20, 1, 1, f"Ball Speed: {self.ball_speed_at_goal:.2f} km/h", self.game_interface.renderer.lime())
        self.game_interface.renderer.end_rendering()

    def clear_text(self):
        self.game_interface.renderer.begin_rendering()
        self.game_interface.renderer.draw_string_2d(20, 20, 1, 1, "", self.game_interface.renderer.lime())
        self.game_interface.renderer.end_rendering()

if __name__ == "__main__":
    goal_speed = GoalSpeed()
    goal_speed.start()
