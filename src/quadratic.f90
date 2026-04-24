subroutine quadratic(a, b, c, x1, x2, status)
   implicit none

   real, intent(in) :: a, b, c
   real, intent(out) :: x1, x2
   integer, intent(out) :: status

   real disc, tol

   tol = EPSILON(1.0)

   if (a == 0) then
      status = 0
      return
   end if

   disc = b*b - 4*a*c

   if (disc > tol) then
      ! There are two real values
      x1 = (-b + sqrt(disc))/(2*a)
      x2 = (-b - sqrt(disc))/(2*a)
      status = 2
   else if (disc < -tol) then
      status = -2
   else
      status = 1
      x1 = -b/(2*a)
      x2 = x1
   end if

end subroutine quadratic

