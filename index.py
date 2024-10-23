import gc
import os

def df():
  s = os.statvfs('//')
  total_memory = 2
  available_memory = (s[0]*s[3])/1048576
  occupied_memory = total_memory-available_memory
  occupied_percentage = (occupied_memory / total_memory) * 100
  available_percentage = (available_memory / total_memory) * 100
  
    # Print the results
  print(f"Total Memory: {total_memory} MB")
  print(f"Occupied Memory: {occupied_memory} MB ({occupied_percentage:.2f}%)")
  print(f"Available Memory: {available_memory} MB ({available_percentage:.2f}%)")

def free(full=False):
  F = gc.mem_free()
  
  A = gc.mem_alloc()
  print(F,A)
  T = F+A
  P = (F/T*100)

  print( P)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))
free()
df()