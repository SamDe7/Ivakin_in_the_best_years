import random

class Probability:
    def __init__(self):
        self.content_type_weights = {    
            'image': 0.5
        }

    def get_random_content_type(self):
        return random.choices(
            population=list(self.content_type_weights.keys()),
            weights=self.content_type_weights.values(),
            k=1
        )[0]

    def save_or_not(self, content_count: int, max_count: int = 150) -> float:
        if content_count >= max_count:
            return 0.1
        
        fill_ratio_for_saving = content_count / max_count
        return 0.7 * (1 - fill_ratio_for_saving * 0.7)

    def send_or_not(self, content_count: int, max_count: int = 100, min_count: int = 30) -> float:
        if content_count <= min_count:
            return 0.4
        elif content_count > max_count:
            return 0.6
        else:
            fill_ratio_for_sending = (content_count - min_count) / (max_count - min_count)
            return (0.4 + fill_ratio_for_sending * 0.2)
        

probability_manager = Probability()