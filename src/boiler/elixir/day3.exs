defmodule Day3 do
    def print_weird() do
        IO.puts("Weird")
    end
    def print_notweird() do
        IO.puts("Not weird")
    end
    def even(num) when 
        is_integer(num) and num > 6 and num < 20 do
        print_weird()
    end
    def even(_) do
        print_notweird()
    end
    def odd() do
        print_weird()
    end
    def weird_test(num) do
        if ( rem(num, 2) == 0) do
            even(num)
        else
            odd()
        end
    end
    def day3 do
        num = String.to_integer(String.trim(IO.gets("Enter number ")))
        weird_test(num)
    end
end
