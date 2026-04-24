subroutine sub(a, b, o)
   implicit none

   real, intent(in) :: a, b
   real, intent(out) :: o

   o = a - b
end subroutine sub

