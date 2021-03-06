import xml.dom.minidom
import numpy
import string

def CreateLib():
    """@todo: document me"""
    import sys
    import time
    domimpl = xml.dom.minidom.getDOMImplementation()
    doc = domimpl.createDocument(None, "source_library", None)
    lib = doc.documentElement
    lib.setAttribute("title", "source library")
    lib.appendChild(doc.createComment('Source library created by %s at %s' %
                                      (sys.argv[0], time.asctime())))
    return lib, doc

def MakeScale(flux_value):
    """Get the scale of the flux value
    ex : 1.4e-14 ---> 1e-14"""
    return 10 ** numpy.floor(numpy.log10(flux_value) + 0.5)
    
    
def addParameter(el, name, free, value, scale, min, max):
    """Add a parameter to a source"""
    doc = el.ownerDocument
    param = doc.createElement('parameter')
    param.setAttribute('name', name)
    param.setAttribute('free', '%d' % free)
    param.setAttribute('scale', '%g' % scale)
    param.setAttribute('value', '%g' % value)
    param.setAttribute('max', '%g' % max)
    param.setAttribute('min', '%g' % min)
    el.appendChild(param)


def AddPointLike(doc,ra,dec):
    spatial = doc.createElement('spatialModel')
    spatial.setAttribute('type', 'SkyDirFunction')
    addParameter(spatial, 'RA', 0, ra, 1.0, -360.0, 360.0)
    addParameter(spatial, 'DEC', 0, dec, 1.0, -90.0, 90.0)
    return spatial

def AddDisk(doc,ra,dec,radius):
    spatial = doc.createElement('spatialModel')
    spatial.setAttribute('type', 'DiskFunction')
    addParameter(spatial, 'RA', 0, ra, 1.0, -360.0, 360.0)
    addParameter(spatial, 'DEC', 0, dec, 1.0, -90.0, 90.0)
    addParameter(spatial, 'Radius', 1, radius, 1., 0.01, 10.0)
    return spatial

def AddGauss(doc,ra,dec,radius):
    spatial = doc.createElement('spatialModel')
    spatial.setAttribute('type', 'GaussFunction')
    addParameter(spatial, 'RA', 0, ra, 1.0, -360.0, 360.0)
    addParameter(spatial, 'DEC', 0, dec, 1.0, -90.0, 90.0)
    addParameter(spatial, 'Sigma', 1, radius, 1., 0.01, 10.0)
    return spatial


def AddShell(doc,ra,dec,radius,width):
    spatial = doc.createElement('spatialModel')
    spatial.setAttribute('type', 'ShellFunction')
    addParameter(spatial, 'RA', 0, ra, 1.0, -360.0, 360.0)
    addParameter(spatial, 'DEC', 0, dec, 1.0, -90.0, 90.0)
    addParameter(spatial, 'Radius', 1, radius, 1., 0.01, 10.0)
    addParameter(spatial, 'Width', 1, width, 1., 0.01, 10.0)
    return spatial
    
    
def AddEllipticalDisk(doc,ra,dec,PA,MinorRadius,MajorRadius):
    spatial = doc.createElement('spatialModel')
    spatial.setAttribute('type', 'EllipticalDisk')
    addParameter(spatial, 'RA', 0, ra, 1.0, -360.0, 360.0)
    addParameter(spatial, 'DEC', 0, dec, 1.0, -90.0, 90.0)
    addParameter(spatial, 'PA', 0, PA, 1.0, -360.0, 360.0)
    addParameter(spatial, 'MinorRadius', 1, MinorRadius, 1., 0.001, 10.0)
    addParameter(spatial, 'MajorRadius', 1, MajorRadius, 1., 0.001, 10.0)
    return spatial

def AddEllipticalGauss(doc,ra,dec,PA,MinorRadius,MajorRadius):
    spatial = doc.createElement('spatialModel')
    spatial.setAttribute('type', 'EllipticalGauss')
    addParameter(spatial, 'RA', 0, ra, 1.0, -360.0, 360.0)
    addParameter(spatial, 'DEC', 0, dec, 1.0, -90.0, 90.0)
    addParameter(spatial, 'PA', 1, PA, 1.0, -360.0, 360.0)
    addParameter(spatial, 'MinorRadius', 1, MinorRadius, 1., 0.001, 10.0)
    addParameter(spatial, 'MajorRadius', 1, MajorRadius, 1., 0.001, 10.0)
    return spatial

def AddConstantValue(doc,value):
    spatial = doc.createElement('spatialModel')
    spatial.setAttribute('type', 'ConstantValue')
    addParameter(spatial, 'Value', 1, value, 1.0, 0.001, 100.0)
    return spatial

def AddSpatialMap(doc,value,file = "map.fits"):
    spatial = doc.createElement('spatialModel')
    spatial.setAttribute('type', 'SpatialMap')
    spatial.setAttribute('file', file)
    addParameter(spatial, 'Prefactor', 1, value, 1.0, 0.001, 100.0)
    return spatial

def AddMapCube(doc,value,file = "map.fits"):
    spatial = doc.createElement('spatialModel')
    spatial.setAttribute('type', 'MapCubeFunction')
    spatial.setAttribute('file', file)
    addParameter(spatial, 'Normalization', 1, value, 1.0, 0.001, 100.0)
    return spatial


def addCTABackgroundGauss(lib):
    doc = lib.ownerDocument
    src = doc.createElement('source')
    src.setAttribute('name', "Background")
    src.setAttribute('type', "RadialAcceptance")
    src.setAttribute('instrument', "CTA")
    radmod = doc.createElement('radialModel')
    radmod.setAttribute('type', 'Gaussian')
    addParameter(radmod,'Sigma',1,3.0,1,0.01,10)
    src.appendChild(radmod)
    return src
    

def addCTABackgroundProfile(lib, width= 1.5,core = 3, tail =5.):
    doc = lib.ownerDocument
    src = doc.createElement('source')
    src.setAttribute('name', "Background")
    src.setAttribute('type', "RadialAcceptance")
    src.setAttribute('instrument', "CTA")
    radmod = doc.createElement('radialModel')
    radmod.setAttribute('type', 'Profile')
    addParameter(radmod,'Width',1,width,1,0.1,1000)
    addParameter(radmod,'Core',1,core,1,0.1,1000)
    addParameter(radmod,'Tail',1,tail,1,0.1,1000)
    src.appendChild(radmod)
    return src
    
def addCTABackgroundPolynom(lib, Coeff, Coeff_free):
    doc = lib.ownerDocument
    src = doc.createElement('source')
    src.setAttribute('name', "Background")
    src.setAttribute('type', "RadialAcceptance")
    src.setAttribute('instrument', "CTA")
    radmod = doc.createElement('radialModel')
    radmod.setAttribute('type', 'Polynom')
    for i in xrange(len(Coeff)):
        try :
            addParameter(radmod,'Coeff'+str(i),Coeff_free[i],Coeff[i],1,-10,10)
        except :
            addParameter(radmod,'Coeff'+str(i),1,Coeff[i],1,-10,10)
    src.appendChild(radmod)
    return src

def addCTAIrfBackground(lib):
    doc = lib.ownerDocument
    src = doc.createElement('source')
    src.setAttribute('name', "CTABackgroundModel")
    src.setAttribute('type', "CTAIrfBackground")
    src.setAttribute('instrument', "CTA")
    
    spec = doc.createElement('spectrum')
    spec.setAttribute('type', 'PowerLaw')
    addParameter(spec, 'Prefactor',1, 1, 1, 1e-3, 1e3)
    addParameter(spec, 'Index', 1, 0, 1.0, -5,5)
    addParameter(spec, 'PivotEnergy', 0, 1., 1.e6, 0.01, 1e3)
    src.appendChild(spec)

    return src

def addCTACubeBackground(lib):
    doc = lib.ownerDocument
    src = doc.createElement('source')
    src.setAttribute('name', "CTABackgroundModel")
    src.setAttribute('type', "CTACubeBackground")
    src.setAttribute('instrument', "CTA")
    
    spec = doc.createElement('spectrum')
    spec.setAttribute('type', 'PowerLaw')
    addParameter(spec, 'Prefactor',1, 1, 1, 1e-3, 1e3)
    addParameter(spec, 'Index', 1, 0, 1.0, -5,5)
    addParameter(spec, 'PivotEnergy', 0, 1., 1.e6, 0.01, 1e3)
    src.appendChild(spec)

    return src

def addPowerLaw1(lib, name, type = "PointSource", eflux=0,
                   flux_free=1, flux_value=1e-9, flux_scale=0,
                   flux_max=1000.0, flux_min=1e-5,
                   index_free=1, index_value=-2.0,
                   index_min=-5.0, index_max=-0.5):
    """Add a source with a POWERLAW1 model"""
    elim_min = 30
    elim_max = 3e7
    if flux_scale == 0:
        flux_scale = MakeScale(flux_value)
    flux_value /= flux_scale
    doc = lib.ownerDocument
    src = doc.createElement('source')
    src.setAttribute('name', name)
    src.setAttribute('type', type)
    spec = doc.createElement('spectrum')
    spec.setAttribute('type', 'PowerLaw')
    addParameter(spec, 'Prefactor',
                 flux_free, flux_value, flux_scale, flux_min, flux_max)
    addParameter(spec, 'Index', index_free, index_value, 1.0,
                 index_min, index_max)
    addParameter(spec, 'Scale', 0, eflux, 1.0, elim_min, elim_max)
    src.appendChild(spec)
    return src



def addPowerLaw2(lib, name, type = "PointSource", emin=30, emax=3e7,
                   flux_free=1, flux_value=1.6e-8, flux_scale=0,
                   flux_max=1000.0, flux_min=1e-5,
                   index_free=1, index_value=-2.0,
                   index_min=-5.0, index_max=-0.5):
    """Add a source with a POWERLAW2 model"""
    elim_min = 30
    elim_max = 300000
    if emin < elim_min:
        elim_min = emin
    if emax > elim_max:
        elim_max = emax
    if flux_scale == 0:
        flux_scale = MakeScale(flux_value)
    flux_value /= flux_scale
    doc = lib.ownerDocument
    src = doc.createElement('source')
    src.setAttribute('name', name)
    src.setAttribute('type', type)
    spec = doc.createElement('spectrum')
    spec.setAttribute('type', 'PowerLaw2')
    addParameter(spec, 'Integral',
                 flux_free, flux_value, flux_scale, flux_min, flux_max)
    addParameter(spec, 'Index', index_free, index_value, 1.0,
                 index_min, index_max)
    addParameter(spec, 'LowerLimit', 0, emin, 1.0, elim_min, elim_max)
    addParameter(spec, 'UpperLimit', 0, emax, 1.0, elim_min, elim_max)
    src.appendChild(spec)

    return src


def addLogparabola(lib, name,  type = "PointSource", enorm=300,
                   norm_free=1, norm_value=1e-9, norm_scale=0,
                   norm_max=1000.0, norm_min=1e-5,
                   alpha_free=1, alpha_value=1.0,
                   alpha_min=.5, alpha_max=5.,
                   beta_free=1, beta_value=1.0,
                   beta_min=0.0005, beta_max=5.0):
    """Add a source with a LOGPARABOLA model"""
    elim_min = 30
    elim_max = 3e7

    if enorm == 0:
        enorm = 2e5  # meanEnergy(emin,emax,index_value)
        norm_value *= (enorm / 100.0) ** alpha_value
    if norm_scale == 0:
        norm_scale = MakeScale(norm_value)
    norm_value /= norm_scale
    doc = lib.ownerDocument
    src = doc.createElement('source')
    src.setAttribute('name', name)
    src.setAttribute('type', type)
    spec = doc.createElement('spectrum')
    spec.setAttribute('type', 'LogParabola')
    addParameter(spec, 'norm',
                 norm_free, norm_value, norm_scale, norm_min, norm_max)
    addParameter(spec, 'alpha', alpha_free, alpha_value, 1.0,
                 alpha_min, alpha_max)
    addParameter(spec, 'Eb', 0, enorm, 1.0, elim_min, elim_max)
    addParameter(spec, 'beta', beta_free, beta_value, 1.0, beta_min, beta_max)
    #addParameter(spec, 'Prefactor',
                 #norm_free, norm_value, norm_scale, norm_min, norm_max)
    #addParameter(spec, 'Index', alpha_free, alpha_value, 1.0,
                 #alpha_min, alpha_max)
    #addParameter(spec, 'Curvature', 0, enorm, 1.0, elim_min, elim_max)
    #addParameter(spec, 'Scale', beta_free, beta_value, 1.0, beta_min, beta_max)
    src.appendChild(spec)

    return src

def addExponotialCutOffPL(lib, name,  type = "PointSource", eflux=0,
                   flux_free=1, flux_value=1e-9, flux_scale=0,
                   flux_max=1000.0, flux_min=1e-5,
                   index_free=1, index_value=-2.0,
                   index_min=-5.0, index_max=-0.5,
                   cutoff_free=1, cutoff_value=1e6,
                   cutoff_min=0.01, cutoff_max=1000):
    """Add a source with a Exponentially cut-off power law model"""
    elim_min = 30
    elim_max = 3e7

    elim_min = 30
    elim_max = 3e7
    if flux_scale == 0:
        flux_scale = MakeScale(flux_value)
    flux_value /= flux_scale
    doc = lib.ownerDocument
    src = doc.createElement('source')
    src.setAttribute('name', name)
    src.setAttribute('type', type)
    spec = doc.createElement('spectrum')
    spec.setAttribute('type', 'ExpCutoff')
    addParameter(spec, 'Prefactor',
                 flux_free, flux_value, flux_scale, flux_min, flux_max)
    addParameter(spec, 'Index', index_free, index_value, 1.0,
                 index_min, index_max)
    addParameter(spec, 'Scale', 0, eflux, 1.0, elim_min, elim_max)
    addParameter(spec, 'Cutoff', cutoff_free, cutoff_value, 1.0, cutoff_min, cutoff_max)
    src.appendChild(spec)

    return src


def addGaussian(lib, name, type = "PointSource",norm_scale=0,
                   norm_free=1, norm_value=1e-10, 
                   norm_max=1000.0, norm_min=1e-5,
                   mean_free=1, mean_value=5.0,mean_scale=0,
                   mean_min=0.01, mean_max=100,
                   sigma_free=1, sigma_value=1.0,sigma_scale=0,
                   sigma_min=0.01, sigma_max=100):
    """Add a source with a Gaussian model"""
    elim_min = 30
    elim_max = 3e7
    if norm_scale == 0:
        norm_scale = MakeScale(norm_value)
    norm_value /= norm_scale
    if mean_scale == 0:
        mean_scale = MakeScale(mean_value)
    mean_value /= mean_scale
    if sigma_scale == 0:
        sigma_scale = MakeScale(sigma_value)
    sigma_value /= sigma_scale
    
    
    doc = lib.ownerDocument
    src = doc.createElement('source')
    src.setAttribute('name', name)
    src.setAttribute('type', type)
    spec = doc.createElement('spectrum')
    spec.setAttribute('type', 'Gaussian')
    addParameter(spec, 'Normalization',norm_free, norm_value, norm_scale, norm_min, norm_max)
    addParameter(spec, 'Mean', mean_free, mean_value, mean_scale, mean_min, mean_max)
    addParameter(spec, 'Sigma', sigma_free, sigma_value, sigma_scale, sigma_min, sigma_max)
    src.appendChild(spec)
    return src

