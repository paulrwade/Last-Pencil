import string

my_username = str(input())

my_template = string.Template("Dear $username! It was really nice to meet you. Hopefully, you have a nice day! See you soon, $username!")

output_string = my_template.substitute(username = my_username)

print(output_string)




