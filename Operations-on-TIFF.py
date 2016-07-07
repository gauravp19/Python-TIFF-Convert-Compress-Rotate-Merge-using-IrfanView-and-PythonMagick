from PythonMagick import Image, CompressionType
import os
import datetime
import subprocess
from PIL import Image as RotateOpr


class TiffOpr:
    """
    This class contains methods that perform different operations on TIFFS. The python packages
    used in the implementation of this class are
    PythonMagick - http://www.lfd.uci.edu/~gohlke/pythonlibs/#pythonmagick
    PIL - http://www.pythonware.com/products/pil/
    IrfanView - http://www.irfanview.com/

    The salient features of this class are:

    1) Converting images to TIFF files
    2) Rotating TIFF images
    3) Compressing TIFF files
    4) Creating multi-page TIFF files
    5) Creating multi-page PDFs
    """

    def __init__(self):
        pass

    @staticmethod
    def convert_images_to_tiff(list_of_file_paths, destination_directory, delete_source=False):
        """
        This static method deals with converting images of type .bmp, .jpg, .png to .tiff.
        This method takes parameters they are as follows:
        :param list_of_file_paths: Example: ['C:\Users\gpatil\Desktop\image1.png', 'C:\Users\gpatilSample\image2.png']
        :param destination_directory: The directory where the converted images are to be saved
        :param delete_source: If the delete_source param is set to True then the original files will get erased after
               the conversion is completed
        :return: returns a dictionary containing the invalid file paths passed to the method (if any) and a result_code
                 that has the value 0 or 1 based on the success and failure of the operation
        """
        result_dictionary = {}
        invalid_files_list = []
        for paths in list_of_file_paths:
            if os.path.exists(paths) is False:
                invalid_files_list.append(paths)
                continue
            image_object = Image(paths)
            file_name = os.path.basename(paths)
            name, ext = os.path.splitext(file_name)
            print "Converting Image " + str(file_name) + " to TIFF"
            image_object.write(os.path.join(destination_directory, name + ".tiff"))
            print "Conversion Complete"
        if not invalid_files_list:
            result_dictionary.update({"result_code": 0, "invalid_file_paths": "None"})
        else:
            csv_list_of_invalid_file_paths = ",".join(invalid_files_list)
            result_dictionary.update({"result_code": -1, "invalid_file_paths": csv_list_of_invalid_file_paths})
            print "Following files at paths could not be converted"
            for files in invalid_files_list:
                print files

        if delete_source is True:
            for paths in list_of_file_paths:
                if os.path.exists(paths) is False:
                    invalid_files_list.append(paths)
                    continue
                os.remove(paths)
            print "Legacy files deleted successfully"
        return result_dictionary

    @staticmethod
    def rotate_images(image_path, angle):
        """
        This is a static method that takes the path of the image and the angle to rotate the image. This method
        overwrites the image that is passed as a param.
        :param image_path: Example : 'C:\Users\gpatil\Desktop\image1.png'
        :param angle: Example for rotating the image right pass -90 and for rotating the image left pass 90
        """
        ang = int(angle)
        image = RotateOpr.open(image_path)
        image = image.rotate(ang, expand=True)
        image.save(image_path)


    @staticmethod
    def compress_tiff_files(list_of_file_paths, destination_directory, delete_source=False):
        """
        This method deals with compression of TIFF images. ZipCompression algorithm is used from the PythonMagick
        library.
        :param list_of_file_paths: ['C:\Users\gpatil\Desktop\image1.tiff', 'C:\Users\gpatilSample\image2.tiff']
        :param destination_directory: 'C:\Users\gpatil\Desktop\image1.png'
        :param delete_source: If the delete_source param is set to True then the original files will get
               erased after they are compressed
        :return: returns a dictionary containing the invalid file paths passed to the method (if any) and a result_code
                 that has the value 0 or 1 based on the success and failure of the operation
        """
        result_dictionary = {}
        invalid_files_list = []
        for paths in list_of_file_paths:
            if os.path.exists(paths) is False:
                invalid_files_list.append(paths)
                continue
            image_object = Image(paths)
            image_object.compressType(CompressionType.ZipCompression)
            file_name = os.path.basename(paths)
            print "Compressing Image" + str(file_name) + " to TIFF"
            image_object.write(os.path.join(destination_directory, file_name))
            print "Compression Complete"
        if not invalid_files_list:
            result_dictionary.update({"result_code": 0, "invalid_file_paths": "None"})
        else:
            csv_list_of_invalid_file_paths = ",".join(invalid_files_list)
            result_dictionary.update({"result_code": -1, "invalid_file_paths": csv_list_of_invalid_file_paths})
            print "Following files at paths could not be compressed"
            for files in invalid_files_list:
                print files
        if delete_source is True:
            for files in list_of_file_paths:
                if os.path.exists(paths) is False:
                    invalid_files_list.append(paths)
                    continue
                os.remove(files)
                print "Legacy files deleted successfully"
        return result_dictionary

    @staticmethod
    def create_multi_page_tiffs(list_of_file_paths, destination_directory, delete_source=False):
        """
        This method appends multiple tiffs into a single tiff file similar to that of a multi-page pdf
        document.
        :param list_of_file_paths: ['C:\Users\gpatil\Desktop\image1.tiff', 'C:\Users\gpatilSample\image2.tiff']
        :param destination_directory: 'C:\Users\gpatil\Desktop\image1.png'
        :param delete_source: returns a dictionary containing the invalid file paths passed to the method (if any)
               and a result_code that has the value 0 or 1 based on the success and failure of the operation
        :return: returns a dictionary containing the invalid file paths passed to the method (if any) and a result_code
                 that has the value 0 or 1 based on the success and failure of the operation
        """
        result_dictionary = {}
        valid_file_paths = []
        invalid_file_paths = []
        for files in list_of_file_paths:
            if os.path.exists(files):
                valid_file_paths.append(files)
            else:
                invalid_file_paths.append(files)
        if not invalid_file_paths:
            result_dictionary.update({"result_code": 0, "invalid_file_paths": "None"})
        else:
            csv_list_of_invalid_file_paths = ",".join(invalid_file_paths)
            result_dictionary.update({"result_code": -1, "invalid_file_paths": csv_list_of_invalid_file_paths})
        csv_file_names = ",".join(valid_file_paths)
        merged_tiff_filename = "Merge" + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + ".tiff"
        merged_filename = os.path.join(destination_directory, merged_tiff_filename)
        os.environ["PATH"] = os.environ["PATH"] + ";" + os.path.join(os.path.join(os.getcwd(), "ImageProcessing"),
                                                                     "IrfanViewPortable.exe")
        software_path = os.path.join(os.path.join(os.getcwd(), "ImageProcessing"), "i_view32.exe")
        subprocess.Popen(software_path + " /multitif=" + "(" + merged_filename + "," + csv_file_names + ") /killmesoftly /silent", shell=True,
                         stdout=subprocess.PIPE,  env={'PATH': os.getenv('PATH')}).stdout.read()
        if delete_source is True:
            for files in valid_file_paths:
                os.remove(files)
                print "Legacy files deleted successfully"
        return result_dictionary

    @staticmethod
    def create_multi_page_pdf(list_of_file_paths, destination_directory, delete_source=False):
        """
        This method appends multiple images into a single PDF file
        document. 
        :param list_of_file_paths: ['C:\Users\gpatil\Desktop\image1.tiff', 'C:\Users\gpatilSample\image2.tiff']
        :param destination_directory: 'C:\Users\gpatil\Desktop\image1.png'
        :param delete_source: returns a dictionary containing the invalid file paths passed to the method (if any)
               and a result_code that has the value 0 or 1 based on the success and failure of the operation
        :return: returns a dictionary containing the invalid file paths passed to the method (if any) and a result_code
                 that has the value 0 or 1 based on the success and failure of the operation
        """
        result_dictionary = {}
        valid_file_paths = []
        invalid_file_paths = []
        for files in list_of_file_paths:
            if os.path.exists(files):
                valid_file_paths.append(files)
            else:
                invalid_file_paths.append(files)
        if not invalid_file_paths:
            result_dictionary.update({"result_code": 0, "invalid_file_paths": "None"})
        else:
            csv_list_of_invalid_file_paths = ",".join(invalid_file_paths)
            result_dictionary.update({"result_code": -1, "invalid_file_paths": csv_list_of_invalid_file_paths})
        csv_file_names = ",".join(valid_file_paths)
        merged_pdf_filename = "Merge" + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + ".pdf"
        merged_filename = os.path.join(destination_directory, merged_pdf_filename)
        software_path = os.path.join(os.path.join(os.getcwd(), "ImageProcessing"), "i_view32.exe")
        subprocess.Popen(software_path + " /multipdf=" + "(" + merged_filename + "," + csv_file_names + ") /killmesoftly /silent", shell=True,
                         stdout=subprocess.PIPE,  env={'PATH': os.getenv('PATH')}).stdout.read()
        if delete_source is True:
            for files in valid_file_paths:
                os.remove(files)
                print "Legacy files deleted successfully"
        return result_dictionary
