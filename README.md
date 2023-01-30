# Dipole-Spectrometer

This reporsitory contains all code used for the calcultations of the energy- and energy spread of the dipole spectrometer at the SEALab accelerator at HZB.

The folder "Trajectories" contains the 3D-field creation file called "3D Field Creation". In that file, the CST field "Dipole.txt" is loaded. 
Using the created 3D file, this can be implemented into ASTRA and the tracking needs to be done. In the file "BFeld Trajectory", the same field is loaded and multiplicated by the factor k that was used in ASTRA. If an other 3D field is used than the one I provided, do not forget to change the offset in the file.
In that file, the effective length of the dipole spectrometer is calculated.

The folder "Calculations" obtains the file "Bachelorarbeit", in which most calculations were performed. In that file, the raw data is analised first. The fit parameters are calculated and the relationships B(I) and I(B) determined. The numerical calculation for the change of B-field in each direction are performed. This error is used for the calculation of number of turns.
Then, the earlier calculated effective length of the dipole spectrometer must be manually inserted. Bapprox(p) calulated the approximate B-field needed for an electron of momentum p to reach the centre of the screen. The factor k from ASTRA must be inserted, so that the real magnetic field is calculated, which will then be implemented into the I(B) calculation. This gives the current needed for a electron of momentum p to reach the screen.
p/I is then calculated. 
This gives the first major result.

The folder "TrafoMatrix" contains the calculations for the transformation matrix. For that, the 3D field from earlier is implemented 
