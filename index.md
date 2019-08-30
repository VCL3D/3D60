<p>
  <img src="./assets/img/Modalities.png" width="100%">
</p>

# Overview
<b>3D60</b> is a collective dataset generated for contacting 360<sup>o</sup> research [<a href="##">1</a>, <a href="##">2</a>, <a href="##">3</a>]. It is composed of renders from existing large-scale 3D datasets (Matterpot3D[<a hyref="##">4</a>], Stanford2D3D[<a hyref="##">5</a>], SunCG[<a hyref="##">6</a>]).

## Motivation
> Modern 3D vision advancements rely on data driven methods and thus, task specific annotated datasets.
> Especially for geometric inference tasks like depth and surface estimation, the collection of high quality data is very challenging, expensive and laborious.
> While considerable efforts have been made for traditional pinhole cameras, the same cannot be said for omnidirectional ones.
> Our __3D60<sup>o</sup>__ dataset fills a very important gap in data-driven spherical 3D vision and namely for monocular and stereo dense depth and surface estimation.
> _We originate by exploiting the efforts made in providing synthetic and real scanned 3D datasets of interior spaces and re-using them via ray-tracing in order to generate high quality, densely annotated spherical panoramas._

## Description

### Formats

<ul>
  <li> <b>RGB</b> images: <code>.png</code> [<b>Invalid pixel values</b>: (64, 64, 64)]</li>
  <li> <b>Depth</b> maps: (float) 1-channel <code>.exr</code><b>[Invalid pixel values</b>:(inf)]</li>
  <li> <b>Surface</b> maps: (float) 3-channel <code>.exr</code> [<b>Invalid pixel values</b>:(0.0, 0.0, 0.0), (nan, nan, nan)]</li>
</ul>

### Camera positions

Regarding Matterport3D and Stanford2D3D we used the existing camera poses to render our dataset, while for SunCG we chose the center of each rendered room, which resulted to rendering artifacts and thus a number of invalid renders.

## Showcase
<p align="center">
  <div> 
    <img src="./assets/img/data_gifs/DatasetGifMatterport.gif" width="32%" style="float:left; margin-right:1%;">
  </div>
  <div> 
    <img src="./assets/img/data_gifs/DatasetGifStanford.gif" width="32%" style="float:left; margin-right:1%;">
  </div>
  <div> 
    <img src="./assets/img/data_gifs/DatasetGifSunCG.gif" width="32%" style="float:left; margin-right:1%;">
  </div>
  <p style="clear:both;"/>
</p>


# Usage

## Download
<p>We follow a <b>two-step</b> procedure to download the <b>3D60</b> dataset.</p>
<ol>
  <li>
    Access to 3D60 dataset requires to agree with the terms and conditions for each of the 3D datasets that were used to create (i.e. render) the 3D60 dataset. Therefore, in order to grant you access to this dataset, we need to you to first fill <a href="https://docs.google.com/forms/d/e/1FAIpQLSfJBX2LYFlA7ZWBgSAPOWKlem3hEoxsh04Iju_ePARWVWa-vA/alreadyresponded">this</a> request form
  </li>
  <li>
    Then you can request to download the dataset from the host-repository <a href="">Zenodo</a>. The dataset is split into three volumes (due to data-size limitations). The three volumes contain the Up, Left-Down and Right camera poses respectively.
  </li>
</ol>
<p>
Each volume is broken down in several <code>.zip</code> files (4GB each) for more convinient downloading on low bandwidth connections. You need all the <code>.zip</code> archives of each volume in order to extract the containing files.
</p>
<p>
  Data-splits:
</p>

<p>
  We provide the train, validation and test-splits that we used for each related research task that used parts of the 3D60 dataset:
</p>
<p>
 <ul>
   <li>Omnidepth: Dense Depth Estimation for Indoors Spherical Panoramas</li>
   <li>Spherical View Synthesis</li>
   <li>360<sup>o</sup> Surface Regression with a Hyper-Sphere Loss</li>
 </ul>
</p>

## Organization


## Tools

# Bibliography

## Citations


## References


