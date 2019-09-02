<p>
  <img src="./assets/img/Modalities.png" width="100%">
</p>

# Overview
__3D60__ is a collective dataset generated for contacting 360<sup>o</sup> research __\[[1](#ref_omnidepth)]\]__, __\[[2](#ref_svs)\]__, __\[[3](#ref_hypersphere)\]__. 
It comprises multi-modal stereo renders of scenes from realistic and synthetic large-scale 3D datasets (Matterport3D __\[[4](#Matterport3D)\]__, Stanford2D3D __\[[5](#ref_stanford)\]__, SunCG __\[[6](#ref_suncg)\]__).

## Motivation
> Modern 3D vision advancements rely on data driven methods and thus, task specific annotated datasets.
> Especially for geometric inference tasks like depth and surface estimation, the collection of high quality data is very challenging, expensive and laborious.
> While considerable efforts have been made for traditional pinhole cameras, the same cannot be said for omnidirectional ones.
> Our __3D60<sup>o</sup>__ dataset fills a very important gap in data-driven spherical 3D vision and, more specifically, for monocular and stereo dense depth and surface estimation.
> _We originate by exploiting the efforts made in providing synthetic and real scanned 3D datasets of interior spaces and re-using them via ray-tracing in order to generate high quality, densely annotated spherical panoramas._

## Description

### Formats
We offer 3 different modalities as indicated below, with the corresponding data formats following and the invalid values (due to imperfect scanning, holes manifest during rendering) denoted in brackets.

| __Image Type__        | __Data Format__           | __Invalid Value__  |
| ------------- |:-------------:|:-----:|
| `Color` images | <code>.png</code> | gray, _i.e._ `(64, 64, 64)` |
| `Depth` maps | single channel, floating point <code>.exr</code> | `(inf)` |
| `Normal` maps | 3-channel (_x, y, z_), floating point <code>.exr</code> | `(0.0f, 0.0f, 0.0f)` & `(nan, nan, nan)` |

### Camera positions
<p style="text-align: justify;">
Our spherical panoramas are generated using the provided camera poses for Matterport3D and Stanford2D3D, while for SunCG we render from the center of the bounding box of each building, which resulted to rendering artifacts and thus a number of invalid renders.
</p>

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
<p style="text-align: justify;">
<p>We follow a <b>two-step</b> procedure to download the <b>3D60</b> dataset.</p>
<p style="text-align: justify;">
<ol>
  <li>
    Access to 3D60 dataset requires to agree with the terms and conditions for each of the 3D datasets that were used to create (i.e. render) the 3D60 dataset. Therefore, in order to grant you access to this dataset, we need to you to first fill <a href="https://drive.google.com/open?id=1qvo9le8TViOTUzJzcwdP0jUZUN90dWBzD-qcKisXe-w">this</a> request form
  </li>
  <li>
    Then you can request to download the dataset from the host-repository <a href="">Zenodo</a>. The dataset is split into three volumes (due to data-size limitations). The three volumes contain the Up, Left-Down (<i>i.e.</i> Center) and Right viewpoints respectively.
  </li>
</ol>
</p>
<p style="text-align: justify;">
  <b>Note</b> that only completing one step of the two (<i>i.e.</i> only filling out the form, or only requesting access from the Zenodo repositories <b>will not</b> be enough to get access to the data. We will do our best to contact you in such cases and notify you to complete all steps as needed, but our mails may be lost (e.g. spam filters/folders). 
  The only exception to this, is if you have already filled in the form and need access to another Zenodo repository (for example you need extra viewpoint renders which are hosted on different Zenodo repositories), then you only need to fill in the Zenodo request but please, make sure to mention that the form has already been filled in so that we can verify it.
</p>

<p style="text-align: justify;">
Each volume is broken down in several <code>.zip</code> files (4GB each) for more convinient downloading on low bandwidth connections. You need all the <code>.zip</code> archives of each volume in order to extract the containing files.
</p>

## Data-splits:

</p>
<p style="text-align: justify;">
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
<p>
  <img src="./assets/img/DirectoryStruct.png" width="20%">
</p>


## Tools

# Bibliography

## Citations


## References
<a name="OmniDepth"/>__[1]__ Zioulis, N.__\*__, Karakottas, A.__\*__, Zarpalas, D., & Daras, P. (2018). [Omnidepth: Dense depth estimation for indoors spherical panoramas](https://arxiv.org/pdf/1807.09620.pdf). In Proceedings of the European Conference on Computer Vision (ECCV) (pp. 448-465).

<a name="SVS"/>__[2]__ Zioulis, N., Karakottas, A., Zarpalas, D., Alvarez, F., & Daras, P. (2019). [Spherical View Synthesis for Self-Supervised 360<sup>o</sup> Depth Estimation](https://arxiv.org/). In Proceedings of the International Conference on 3D Vision (3DV).

<a name="HyperSphere"/>__[3]__ Karakottas, A., Zioulis, N., Samaras, S., Ataloglou, D., Gkitsas, V., Zarpalas, D., & Daras, P. (2019). [360<sup>o</sup> Surface Regression with a Hyper-sphere Loss](https://arxiv.org/). In Proceedings of the International Conference on 3D Vision (3DV).

<a name="Matterport3D"/> __[4]__ Chang, A., Dai, A., Funkhouser, T., Halber, M., Niessner, M., Savva, M., Song, S., Zeng, A. and Zhang, Y. (2017). [Matterport3d: Learning from rgb-d data in indoor environments](https://niessner.github.io/Matterport/). In Proceedings of the International Conference on 3D Vision (3DV).

<p id="ref_stanford" style="text-align: justify;">
[<a href="http://buildingparser.stanford.edu/dataset.html">5</a>] Armeni, I., Sax, S., Zamir, A.R. and Savarese, S., 2017. Joint 2d-3d-semantic data for indoor scene understanding. arXiv preprint arXiv:1702.01105.
</p>
<p id="ref_suncg" style="text-align: justify;">
[<a href="https://sscnet.cs.princeton.edu/">5</a>] Song, S., Yu, F., Zeng, A., Chang, A.X., Savva, M. and Funkhouser, T., 2017. Semantic scene completion from a single depth image. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (pp. 1746-1754).

<!--
<p style="text-align: justify">
<p id="ref_omnidepth">
[<a href="https://arxiv.org/abs/1807.09620">1</a>] Zioulis, N., Karakottas, A., Zarpalas, D. and Daras, P., 2018. Omnidepth: Dense depth estimation for indoors spherical panoramas. In Proceedings of the European Conference on Computer Vision (ECCV) (pp. 448-465).
</p>
<p id="ref_svs" style="text-align: justify;">
[<a href="##">2</a>]
</p>
<p id="ref_hypersphere" style="text-align: justify;">
[<a href="##">3</a>]
</p>
<p id="ref_matterport" style="text-align: justify;">
[<a href="https://niessner.github.io/Matterport/">4</a>] Chang, A., Dai, A., Funkhouser, T., Halber, M., Niessner, M., Savva, M., Song, S., Zeng, A. and Zhang, Y., 2017. Matterport3d: Learning from rgb-d data in indoor environments. arXiv preprint arXiv:1709.06158.
</p>
<p id="ref_stanford" style="text-align: justify;">
[<a href="http://buildingparser.stanford.edu/dataset.html">5</a>] Armeni, I., Sax, S., Zamir, A.R. and Savarese, S., 2017. Joint 2d-3d-semantic data for indoor scene understanding. arXiv preprint arXiv:1702.01105.
</p>
<p id="ref_suncg" style="text-align: justify;">
[<a href="https://sscnet.cs.princeton.edu/">5</a>] Song, S., Yu, F., Zeng, A., Chang, A.X., Savva, M. and Funkhouser, T., 2017. Semantic scene completion from a single depth image. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (pp. 1746-1754).
</p>
</p>
-->
