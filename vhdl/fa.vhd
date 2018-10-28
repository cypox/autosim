library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity FA is
    Port ( 
           A : in STD_LOGIC;
           B : in STD_LOGIC;
           Cin : in STD_LOGIC;
           S : out STD_LOGIC;
           Co : out STD_LOGIC);
end FA;

architecture Behavioral of fa is

begin

S <= A XOR B XOR Cin;
Co <= (A AND B) OR (Cin AND A) OR (Cin AND B);

end Behavioral;

