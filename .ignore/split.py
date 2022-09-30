# split[0] is ""

text = "-001-203-1232-22"

for i, line in enumerate(text.split("-")):
  print("{}; {}".format(i, line))

# 0; 
# 1; 001
# 2; 203
# 3; 1232
# 4; 22
