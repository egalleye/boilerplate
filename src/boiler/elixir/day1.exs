defmodule ElixirDay1 do
    def day1 do
        x = 4
        y = 4.0
        z = "Elixir is"
        xin = String.to_integer(String.strip(IO.gets "Enter an int"))
        yin = String.to_float(String.strip(IO.gets "Enter a dub"))
        zin = IO.gets "Enter thoughts on Elixir"
        IO.puts "Hello world!"
        xtotal = x + xin
        ytotal = y + yin
        IO.puts (xtotal)
        IO.puts (ytotal)
        IO.puts ([z, " ", zin])
    end
end
