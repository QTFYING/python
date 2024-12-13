# main_script.py
import my_module

def main():
    print("这是main函数, 来自于 main_script")
    my_module.my_function()

print(f"main_script的__name__值为: {__name__}")

if __name__ == "__main__":
    main()