defmodule Day4 do
    def my_age(age) when
        age < 0 do
            IO.puts("Negative age is invalid, please resubmit!")
            day4()
    end
    def my_age(age) when
        age < 13 do
            IO.puts("You are young")
    end 
    def my_age(age) when
        age < 18 and age > 12 do
            IO.puts("You are a teenager")
    end
    def my_age(_) do
        IO.puts("You are old")
    end
    def day4 do
        age = String.to_integer(String.trim(IO.gets("Enter your age, please! ")))
        my_age(age)
    end
end
