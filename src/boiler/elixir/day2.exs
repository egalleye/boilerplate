defmodule ElixirDay2 do
    def write_hello(num) when 
        is_integer(num) and num > 0 do
        IO.puts ("hello world")
        write_hello(num-1)
    end
    def write_hello(_) do
        :ok
    end
    def daytwo do
        IO.puts "Hello yo"
        num = String.to_integer(String.trim(IO.gets ("Enter number")))      
        write_hello(num)
    end
end
