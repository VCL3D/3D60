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

# Formats

<ul>
  <li> <b>RGB</b> images: <code>.png</code> [<b>Invalid pixel values</b>: (64, 64, 64)]</li>
  <li> <b>Depth</b> maps: (float) 1-channel <code>.exr</code><b>[Invalid pixel values</b>:(inf)]</li>
  <li> <b>Surface</b> maps: (float) 3-channel <code>.exr</code> [<b>Invalid pixel values</b>:(0.0, 0.0, 0.0), (nan, nan, nan)]</li>
</ul>

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


## Organization


## Tools

# Bibliography

## Citations


## References


