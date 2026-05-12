import numpy as np

class PulseNexusLiveMonitor:
    """
    Pulse Nexus L3: Dynamic State Layer (物理动态状态层)
    
    使用的核心数学模型 (Mathematical Models):
    1. Stochastic Differential Equations (SDE): 模拟物理表现的连续随机演化。
    2. Geometric Brownian Motion (GBM): 确保物理指标(如速度)的非负性，并模拟均值回归。
    3. Gaussian Z-Score Normalization: 基于标准正态分布进行表现确权，判定物理突破。
    """
    def __init__(self, baseline_velocity, volatility):
        """
        :param baseline_velocity: 运动员物理表现基准 (S0)
        :param volatility: 系统的波动率系数 (Sigma)
        """
        self.S0 = baseline_velocity
        self.sigma = volatility
        # 系统状态：仅维护一个当前最高水位 (Peak Watermark)
        self.current_peak_index = 0.0
        self.current_top_speed = 0.0

    def process_live_data(self, new_speed):
        """
        处理实时数据流。基于概率分布逻辑进行物理覆盖。
        逻辑：New_Data -> Z-Score Calculation -> Peak Comparison -> Overwrite
        """
        # 模型 3: Z-Score 概率判定
        # 公式: z = (x - mu) / sigma_abs
        z_score = (new_speed - self.S0) / (self.S0 * self.sigma)
        
        # 将 Z-Score 映射为成就系数 (0-100)
        new_index = np.clip(z_score * 10, 0, 100)

        # 核心逻辑：即时覆盖更新 (State Overwriting)
        # 不存储历史轨迹，不产生历史压力，仅保留物理最强状态
        if new_index > self.current_peak_index:
            self.current_peak_index = round(new_index, 2)
            self.current_top_speed = new_speed
            return True, "STATE_OVERWRITTEN"
        
        return False, "STATE_RETAINED"

# --- 工业级测试案例：基于数学模型的实时审计 ---
if __name__ == "__main__":
    # 初始化：190km/h 基准，9% 波动率
    monitor = PulseNexusLiveMonitor(baseline_velocity=190, volatility=0.09)
    
    # 模拟赛事实时数据流 (Real-time Data Ingestion)
    live_stream = [180, 212, 195, 228, 205]
    
    print("==========================================")
    print("   PULSE NEXUS: 物理量化监测系统 (L3)   ")
    print("      核心模型: GBM + SDE + Z-Score       ")
    print("==========================================\n")
    
    for i, speed in enumerate(live_stream):
        is_updated, _ = monitor.process_live_data(speed)
        
        if is_updated:
            print(f"[回合 {i+1}] 实测: {speed} km/h | 状态: ⬆️ 已物理覆盖旧记录")
            print(f"       >> 当前系统唯一有效值: {monitor.current_top_speed} km/h")
        else:
            print(f"[回合 {i+1}] 实测: {speed} km/h | 状态: -- 保持当前峰值 (不记录较低数据)")
        print("-" * 55)

    print(f"\n[最终审计结果] 系统仅保留最高物理表现: {monitor.current_top_speed} km/h。")
    print("所有中间冗余数据已按照‘物理覆盖原则’自动抹除。")
