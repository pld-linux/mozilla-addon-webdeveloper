%define		_extension webdeveloper
Summary:	Mozilla Firefox Web Developer Extension
Name:		mozilla-addon-%{_extension}
Version:	0.9.4
Release:	0.19
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/extensions/web_developer/web_developer-%{version}-fx.xpi
# Source0-md5:	ca9e532633bf21dddcff369344e16c60
URL:		http://chrispederick.com/work/firefox/webdeveloper/
Requires:	browser-common(%{_target_cpu})
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_chromedir	%{_datadir}/browser-common/chrome

%description
Adds a menu and a toolbar with various web developer tools.

An essential extension for any web developer/designer as it provides a
raft of incredibly useful features all under one roof. You will wonder
how you ever managed without it!

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_chromedir}

install chrome/*.jar $RPM_BUILD_ROOT%{_chromedir}
# http://www.extensionsmirror.nl/lofiversion/index.php/t228.html
cat <<'EOF' > $RPM_BUILD_ROOT%{_chromedir}/%{_extension}-installed-chrome.txt
content,install,url,jar:resource:/chrome/%{_extension}.jar!/content/%{_extension}/
locale,install,url,jar:resource:/chrome/%{_extension}.jar!/locale/en-US/%{_extension}/
skin,install,url,jar:resource:/chrome/%{_extension}.jar!/skin/classic/%{_extension}/
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- mozilla-firefox
%browser_component_install -b mozilla-firefox -t chrome chrome/webdeveloper{.jar,-installed-chrome.txt}

%triggerun -- mozilla-firefox
%browser_component_uninstall -b mozilla-firefox -t chrome chrome/webdeveloper{.jar,-installed-chrome.txt}

%triggerin -- mozilla
%browser_component_install -b mozilla -t chrome chrome/webdeveloper{.jar,-installed-chrome.txt}

%triggerun -- mozilla
%browser_component_uninstall -b mozilla -t chrome chrome/webdeveloper{.jar,-installed-chrome.txt}

%files
%defattr(644,root,root,755)
%{_chromedir}/*
