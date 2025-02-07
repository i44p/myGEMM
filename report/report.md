# Анализ производительности графических ускорителей NVIDIA GTX 1060 MaxQ и K1

Работа проходила на NVIDIA 1060 MaxQ. Для квадратных матриц размера меньше 256 результаты плохо различимы, поэтому они не попали в выборку. Квадратные матрицы больше 22720+ не перемножались из-за ошибок аллокации памяти (максимально заявленный размер из clinfo - 16384х32768). На GTX 1060 пятое ядро, при work group size=8, выдаёт аномальные знячения, чего не наблюдается на K1. 
Предположительно, такой эффект наблюдается из-за комбинации сниженной частоты ядер MaxQ и частых обращений к локальной памяти при малом размере группы. Это может приводить к слишком задержкам в работе, сопоставимым со втором ядром. Чтобы разобраться подробнее, нужно углублённо аналиировать микроархитектуру MaxQ.
Для визуализации прилагаются срипты на Python. 

![image](https://github.com/user-attachments/assets/443dbf5e-4a47-43d0-9714-88a8006ba5b0)

![image](https://github.com/user-attachments/assets/7e374f78-c26b-40a9-8534-4be0ed096e10)

![image](https://github.com/user-attachments/assets/d505c915-5ec2-46a4-ab0e-651e35c55fe1)

![image](https://github.com/user-attachments/assets/f14e26eb-e55c-4b7f-a78b-083d4e8fe7fa)

![image](https://github.com/user-attachments/assets/b7a4eaff-d2a8-471e-a504-eae0b8852cfb)

![image](https://github.com/user-attachments/assets/ff9cb5e7-4849-4f35-af20-c52b61c525e9)

