from scipy.ndimage import gaussian_filter, maximum_filter
from scipy.ndimage import generate_binary_structure, binary_erosion

### ===========================================================================
class _PeaksDetection:
    def __init__(self, apply_filter:bool=False, threshold=None, sigma=1, filter_type='gaussian'):
        self.apply_filter_ = apply_filter
        self.threshold_ = threshold
        self.sigma_ = sigma
        self.filter_type_ = filter_type
        
    def _apply_filter(self, data):
        if self.filter_type_=='gaussian':
            return gaussian_filter(data, sigma=self.sigma_)
        else:
            raise AttributeError('Requested filter is not implemented')
            
    @staticmethod
    def _get_peaks(image):
        """
        Source: https://stackoverflow.com/a/3689710
        Takes an image and detect the peaks usingthe local maximum filter.
        Returns a boolean mask of the peaks (i.e. 1 when
        the pixel's value is the neighborhood maximum, 0 otherwise)
        """
        # define an 8-connected neighborhood
        neighborhood = generate_binary_structure(2,2)
    
        #apply the local maximum filter; all pixel of maximal value 
        #in their neighborhood are set to 1
        local_max = maximum_filter(image, footprint=neighborhood)==image
        #local_max is a mask that contains the peaks we are 
        #looking for, but also the background.
        #In order to isolate the peaks we must remove the background from the mask.
    
        #we create the mask of the background
        background = (image==0)
    
        #a little technicality: we must erode the background in order to 
        #successfully subtract it form local_max, otherwise a line will 
        #appear along the background border (artifact of the local maximum filter)
        eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
    
        #we obtain the final mask, containing only peaks, 
        #by removing the background from the local_max mask (xor operation)
        detected_peaks = local_max ^ eroded_background
    
        return detected_peaks

        
    def _detect_peaks(self, image):
        image_ = image.copy()
        if self.apply_filter_:
            image_ = self._apply_filter(image_) 
            
        image_filter = image_.copy()
        
        if self.threshold_:
            image_[image_filter<self.threshold_] = 0
            
        return image_filter, self._get_peaks(image_)

    def _xrd_find_peaks(self, XX, YY, image):
        image_filter, detected_peaks = self._detect_peaks(image)
        peaks_x = XX[detected_peaks]
        peaks_y = YY[detected_peaks]
        peaks_z = image[detected_peaks]
        return image_filter, peaks_x, peaks_y, peaks_z
