#HEADFILE
GM/IO2/z=0_mhd_2_n00000100.h                                                    
       4                nProc
       T                IsBinary
       8                nByteReal

#NDIM
       3                nDim

#GRIDBLOCKSIZE
       8                BlockSize1
       8                BlockSize2
       8                BlockSize3

#ROOTBLOCK
       2                nRootBlock1
       1                nRootBlock2
       1                nRootBlock3

#GRIDGEOMETRYLIMIT
cartesian               TypeGeometry
 -2.24000E+02           XyzMin1
  3.20000E+01           XyzMax1
 -6.40000E+01           XyzMin2
  6.40000E+01           XyzMax2
 -6.40000E+01           XyzMin3
  6.40000E+01           XyzMax3

#PERIODIC
       F                IsPeriodic1
       F                IsPeriodic2
       F                IsPeriodic3

#NSTEP
     100                nStep

#TIMESIMULATION
  0.0000000000E+00      TimeSimulation

#NCELL
      4096              nCellPlot

#CELLSIZE
  2.0000000000E+00      CellSizeMin1
  2.0000000000E+00      CellSizeMin2
  2.0000000000E+00      CellSizeMin3

#PLOTRANGE
 -2.2400000000E+02      CoordMin1
  3.2000000000E+01      CoordMax1
 -6.4000000000E+01      CoordMin2
  6.4000000000E+01      CoordMax2
 -1.6000000000E-08      CoordMin3
  1.6000000000E-08      CoordMax3

#PLOTRESOLUTION
 -1.0000000000E+00      DxSavePlot1
 -1.0000000000E+00      DxSavePlot2
 -1.0000000000E+00      DxSavePlot3

#SCALARPARAM
       3                nParam
  6.37800E+06           xsi       
  2.50000E+00           r         
  1.66667E+00           g         

#PLOTVARIABLE
      11                nPlotVar
Rho Ux Uy Uz Bx By Bz P jx jy jz xSI r g
1998-05-01T00:00:00; R R R Mp/cc km/s km/s km/s nT nT nT nPa uA/m2 uA/m2 uA/m2

#OUTPUTFORMAT
real4     

