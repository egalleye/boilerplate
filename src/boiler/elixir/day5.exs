defmodule Day5 do
    def do_mathies(a, b, c, c_tmp, result) when
        c_tmp > 0 do
            exponent = c - c_tmp
            result =
              if (exponent == 0) do
                  a + (:math.pow(2, exponent) * b)
              else
                  result + (:math.pow(2, exponent) * b)
              end
            IO.puts(result)
            do_mathies(a, b, c, c_tmp - 1, result)
    end
    def do_mathies(_, _, _, _, _) do
        :ok
    end
    def day5 do
        a = String.to_integer(String.trim(IO.gets("Please enter value a ")))
        b = String.to_integer(String.trim(IO.gets("Please enter value b ")))
        c = String.to_integer(String.trim(IO.gets("Please enter value c ")))
        c_tmp = c
        do_mathies(a, b, c, c_tmp, 0)
    end
end
