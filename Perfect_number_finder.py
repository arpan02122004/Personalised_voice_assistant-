factors = int(input('Enter the number : '))
x = 0
for i in range(1, factors):
    if  factors % i == 0 :
         x += i 
    print(i)
    if x == factors:
            print(f'{factors} is a perfect number . ')
    else:
        print('The number is not a perfect number . ')
