#minimize { 1@4,I : outlier(I) }.
#minimize { OV@3,B1,B2,F : box_overlap(B1, B2), overlap(B1, B2, F, OV) }.
#minimize { IM@2,B : impurity(B,IM) }.