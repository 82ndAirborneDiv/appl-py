from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def write_manifest(app, ipa_full_url, display_image_url, full_size_image_url):

    bundle_id = app.ios_project.bundle_id
    bundle_version = '{0}.{1}.{2}.{3}'.format(app.major_version,app.minor_version,app.point_version,app.build_version)
    app_title = app.ios_project.project_overview.project.title

    file = open('manifest.plist', 'w')

    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
    file.write('<plist version="1.0">\n')
    file.write('    <dict>\n')
    file.write('        <key>items</key>\n')
    file.write('            <array>\n')
    file.write('                <dict>\n')
    file.write('                    <key>assets</key>\n')
    file.write('                    <array>\n')
    file.write('                    <dict>\n')
    file.write('                    	<key>kind</key>\n')
    file.write('                    	<string>software-package</string>\n')
    file.write('                    	<key>url</key>\n')
    file.write('                    	<string>'+ipa_full_url+'</string>\n')
    file.write('                    <dict>\n')
    file.write('                    <dict>\n')
    file.write('                    	<key>kind</key>\n')
    file.write('                    	<string>display-image</string>\n')
    file.write('                    	<key>url</key>\n')
    file.write('                    	<string>'+display_image_url+'</string>\n')
    file.write('                    </dict>\n')
    file.write('                    <dict>\n')
    file.write('                    	<key>kind</key>\n')
    file.write('                    	<string>full-size-image</string>\n')
    file.write('                    	<key>url</key>\n')
    file.write('                    	<string>'+full_size_image_url+'</string>\n')
    file.write('                	</dict>\n')
    file.write('                </array>\n')
    file.write('                <key>metadata</key>\n')
    file.write('                <dict>\n')
    file.write('                    <key>bundle-identifier</key>\n')
    file.write('                    <string>'+bundle_id+'</string>\n')
    file.write('                    <key>bundle-version</key>\n')
    file.write('                    <string>'+bundle_version+'</string>\n')
    file.write('                    <key>kind</key>\n')
    file.write('                    <string>software</string>\n')
    file.write('                    <key>title</key>\n')
    file.write('                	<string>'+app_title+'</string>\n')
    file.write('				</dict>\n')
    file.write('			</dict>\n')
    file.write('		</array>\n')
    file.write('	</dict>\n')
    file.write('</plist>\n')
    file.close()

    new_manifest = open('manifest.plist')

    app.manifest_file.save('manifest.plist', File(new_manifest), save=False)
    # new_manifest = app.manifest_file
    # file_name = app.ios_project.project_overview.project.project_code_name
    # manifest_prefix = 'itms-services://?action=download-manifest&url=https://'
    # response = HttpResponse(FileWrapper(new_manifest), content_type='application/x-plist')
    # response['Content-Disposition']='attachment; filename:'+ manifest_prefix + '%s.plist' % file_name