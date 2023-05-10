x = int(input())
a = str()

if(x <= 1):
  print(0)
  
  
elif(x == 2):
  
  print(0,1)
else:
  
  y = 0
  z = 1
  
  for i in range(x-2):
    
    c = y + z
    y = z
    z = c
    a = a +" "+ str(c)

  print(f'0 1{a}')