#minimize { 1@4,I : outlier(I) }.
#minimize { OV@3,B1,B2,F : box_overlap(B1, B2), overlap(B1, B2, F, OV) }.
#minimize { 1@2,B,I1,I2 : impurepair(B, I1, I2) }.