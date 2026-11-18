program test_open
  implicit none
  integer :: ierr
  open(10, file='amie.ascii', status='old', form='UNFORMATTED', iostat=ierr)
  if (ierr /= 0) then
     print *, 'Error opening file: ', ierr
  else
     print *, 'Success opening file'
     close(10)
  endif
end program test_open
