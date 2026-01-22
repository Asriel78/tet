import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('assets', exist_ok=True)

threads = [1, 2, 4, 8, 16]
time_static = [91, 53, 28, 20, 18]
time_dynamic_default = [426, 1080, 1125, 1588, 1837]
time_manual = [93, 50, 37, 20, 20]
baseline = 101

speedup_static = [baseline / t for t in time_static]
speedup_manual = [baseline / t for t in time_manual]

plt.figure(figsize=(10, 6))
plt.plot(threads, time_static, 'o-', label='static', linewidth=2, markersize=8)
plt.plot(threads, time_manual, 's-', label='manual', linewidth=2, markersize=8)
plt.xlabel('Число потоков', fontsize=12)
plt.ylabel('Время (мс)', fontsize=12)
plt.title('Зависимость времени от числа потоков (large.pnm)', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xticks(threads)
plt.savefig('assets/graph1_threads_time.png', dpi=150, bbox_inches='tight')
plt.close()

plt.figure(figsize=(10, 6))
plt.plot(threads, speedup_static, 'o-', label='static', linewidth=2, markersize=8)
plt.plot(threads, speedup_manual, 's-', label='manual', linewidth=2, markersize=8)
plt.plot(threads, threads, '--', color='gray', label='ideal', linewidth=1)
plt.xlabel('Число потоков', fontsize=12)
plt.ylabel('Ускорение', fontsize=12)
plt.title('Ускорение относительно однопоточной версии', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xticks(threads)
plt.savefig('assets/graph2_speedup.png', dpi=150, bbox_inches='tight')
plt.close()

chunk_sizes = ['1', '10', '100', '1000', '10000']
time_static_chunk = [21, 22, 21, 20, 21]
time_dynamic_chunk = [1593, 260, 40, 17, 18]

x = np.arange(len(chunk_sizes))
width = 0.35

plt.figure(figsize=(12, 6))
bars1 = plt.bar(x - width/2, time_static_chunk, width, label='static', color='steelblue')
bars2 = plt.bar(x + width/2, time_dynamic_chunk, width, label='dynamic', color='coral')
plt.xlabel('chunk_size', fontsize=12)
plt.ylabel('Время (мс)', fontsize=12)
plt.title('Сравнение schedule при разных chunk_size (8 потоков)', fontsize=14)
plt.xticks(x, chunk_sizes)
plt.legend(fontsize=11)
plt.grid(True, axis='y', alpha=0.3)
plt.yscale('log')
plt.savefig('assets/graph3_chunk_comparison.png', dpi=150, bbox_inches='tight')
plt.close()


plt.figure(figsize=(10, 6))
plt.plot(chunk_sizes, time_dynamic_chunk, 'o-', color='coral', linewidth=2, markersize=8)
plt.axhline(y=20, color='steelblue', linestyle='--', label='static (≈20 мс)')
plt.xlabel('chunk_size', fontsize=12)
plt.ylabel('Время (мс)', fontsize=12)
plt.title('Dynamic schedule: влияние chunk_size (8 потоков)', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.savefig('assets/graph4_dynamic_chunk.png', dpi=150, bbox_inches='tight')
plt.close()

labels = ['single\n(baseline)', 'static\n8 threads', 'dynamic\n8 threads\nchunk=1000', 'manual\n8 threads']
times = [101, 20, 17, 20]
colors = ['gray', 'steelblue', 'coral', 'seagreen']

plt.figure(figsize=(10, 6))
bars = plt.bar(labels, times, color=colors)
plt.ylabel('Время (мс)', fontsize=12)
plt.title('Сравнение всех реализаций (large.pnm)', fontsize=14)
plt.grid(True, axis='y', alpha=0.3)
for bar, time in zip(bars, times):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'{time} мс', ha='center', fontsize=11)
plt.savefig('assets/graph5_all_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

print("Графики сохранены в папку assets/")
print("\nОсновные выводы:")
print(f"- Ускорение static (8 потоков): {baseline/20:.1f}x")
print(f"- Ускорение manual (8 потоков): {baseline/20:.1f}x")
print(f"- Dynamic без chunk_size: катастрофа (overhead > пользы)")
print(f"- Dynamic с chunk_size=1000: лучший результат ({17} мс)")
