args = sys.argv

# further, code of the script "add_four_numbers.py"
sum_o = 0
for index, item in enumerate(args):
    if index == 0:
        continue
    sum_o = sum_o + int(item)

print(sum_o)