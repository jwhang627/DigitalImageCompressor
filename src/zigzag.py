import numpy as np

"""
 Zigzag scan of a matrix
 Argument is a two-dimensional matrix of any size,
 not strictly a square one.
 Function returns a 1-by-(m*n) array,
 where m and n are sizes of an input matrix,
 consisting of its items scanned by a zigzag method.
"""
def zigzag(ipt):
    wmax = ipt.shape[0]
    hmax = ipt.shape[1]
    wmin = 0
    hmin = 0
    w = 0
    h = 0
    i = 0

    output = np.zeros((wmax*hmax))
    while((w<wmax) and (h<hmax)):
        if (((h + w)%2) == 0):
            if (w == wmin):
                output[i] = ipt[w,h]
                if (h == hmax):
                    w += 1
                else:
                    h += 1
                i += 1
            elif ((h == (hmax - 1)) and (w < wmax)):
                output[i] = ipt[w,h]
                w += 1
                i += 1
            elif ((w > wmin) and (h < (hmax - 1))):
                output[i] = ipt[w,h]
                w -= 1
                h += 1
                i += 1

        else:
            if ((w == (wmax-1)) and (h <= (hmax -1))):
                output[i] = ipt[w, h]
                h += 1
                i += 1
            elif (h == hmin):
                output[i] = ipt[w, h] 
                if (w == (wmax-1)):
                    h += 1
                else:
                    w += 1

                i += 1
            elif ((w < wmax -1) and (h > hmin)):
                output[i] = ipt[w, h] 
                w += 1
                h -= 1
                i += 1

        if((w == (wmax - 1)) and (h == (hmax - 1))):
            output[i] = ipt[w,h]
            break

    return output

"""
 Inverse zigzag scan of a matrix
 Arguments are: a 1-by-m*n array, 
 where m & n are vertical & horizontal sizes of an output matrix.
 Function returns a two-dimensional matrix of defined sizes,
 consisting of input array items gathered by a zigzag method.
"""
def izigzag(ipt, vmax, hmax):
    h = 0
    v = 0

    vmin = 0
    hmin = 0

    output = np.zeros((vmax, hmax))

    i = 0

    while ((v < vmax) and (h < hmax)):
        if (((h + v) % 2) == 0):
            if (v == vmin):
                output[v, h] = ipt[i]
                if (h == hmax):
                    v += 1
                else:
                    h += 1                        

                i += 1

            elif ((h == (hmax -1)) and (v < vmax)):
                output[v, h] = ipt[i] 
                v += 1
                i += 1

            elif ((v > vmin) and (h < (hmax -1))):
                output[v, h] = ipt[i] 
                v -= 1
                h += 1
                i += 1
        else:
            if ((v == (vmax -1)) and (h <= (hmax -1))):
                output[v, h] = ipt[i] 
                h += 1
                i += 1
                
            elif (h == hmin):
                output[v, h] = ipt[i] 

                if (v == vmax -1):
                    h += 1
                else:
                    v += 1

                i += 1
                
            elif((v < (vmax -1)) and (h > hmin)):
                output[v, h] = ipt[i] 
                v += 1
                h -= 1
                i += 1

            if ((v == (vmax-1)) and (h == (hmax-1))):
                output[v, h] = ipt[i] 
                break

    return output
