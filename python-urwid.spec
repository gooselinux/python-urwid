%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:          python-urwid
Version:       0.9.9.1
Release:       4%{?dist}
Summary:       Console user interface library

Group:         Development/Libraries
License:       LGPLv2+
URL:           http://excess.org/urwid/
Source0:       http://excess.org/urwid/urwid-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)
Patch1:        %{name}-fix-none-leak.patch
BuildRequires: python2-devel
BuildRequires: python-twisted-core
BuildRequires: pygobject2

%description
Urwid is a Python library for making text console applications.  It has many
features including fluid interface resizing, support for UTF-8 and CJK
encodings, standard and custom text layout modes, simple markup for setting
text attributes, and a powerful, dynamic list box that handles a mix of widget
types.  It is flexible, modular, and leaves the developer in control.

%prep
%setup -q -n urwid-%{version}
find urwid -type f -name "*.py" -exec sed -i -e '/^#!\//, 1d' {} \;
find urwid -type f -name "*.py" -exec chmod 644 {} \;
%patch1 -p1

%build
CFLAGS="%{optflags} -fno-strict-aliasing" %{__python} setup.py build

%check
./test_urwid.py

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --no-compile --root %{buildroot}
rm -f tmpl_tutorial.html
mkdir examples
cp -p *.py examples/
rm -f examples/test_urwid.py examples/docgen_*.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG *.html examples
%{python_sitearch}/urwid
%{python_sitearch}/urwid-%{version}*.egg-info

%changelog
* Mon Aug 22 2011 Andy Grover <agrover@redhat.com> - 0.9.9.1-4
- Fix license in specfile to LGPLv2+ from LGPLv2.1+

* Wed Aug 17 2011 Andy Grover <agrover@redhat.com> - 0.9.9.1-3
* Add fix-none-leak.patch

* Mon Aug 15 2011 Andy Grover <agrover@redhat.com> - 0.9.9.1-2
- Add -fno-strict-aliasing to CFLAGS to fix warnings

* Wed May 19 2010 David Cantrell <dcantrell@redhat.com> - 0.9.9.1-1
- Initial package
