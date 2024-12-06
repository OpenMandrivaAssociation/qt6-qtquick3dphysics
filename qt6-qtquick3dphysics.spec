# As of 6.6.0-beta2, clang 16.0.6, enabling LTO results in
# a link time failure
# fragment is larger than or outside of variable
#   call void @llvm.dbg.declare(metadata ptr undef, metadata !901812, metadata !DIExpression(DW_OP_LLVM_fragment, 384, 96)), !dbg !901860
# !901812 = !DILocalVariable(name: "rayParams", scope: !901793, file: !106324, line: 1425, type: !106827)
# fragment is larger than or outside of variable
#   call void @llvm.dbg.value(metadata float 0.000000e+00, metadata !901812, metadata !DIExpression(DW_OP_LLVM_fragment, 480, 32)), !dbg !901858
# !901812 = !DILocalVariable(name: "rayParams", scope: !901793, file: !106324, line: 1425, type: !106827)
%global _disable_lto 1
#define beta rc2

Name:		qt6-qtquick3dphysics
Version:	6.8.1
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtquick3dphysics.git
Source:		qtquick3dphysics-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtquick3dphysics-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{qtmajor} 3D Library
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6QmlCore)
BuildRequires:	cmake(Qt6QmlModels)
BuildRequires:	cmake(Qt6QmlLocalStorage)
BuildRequires:	cmake(Qt6QmlWorkerScript)
BuildRequires:	cmake(Qt6QmlXmlListModel)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6OpenGLWidgets)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6ShaderTools)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickControls2)
BuildRequires:	cmake(Qt6QuickControls2Impl)
BuildRequires:	cmake(Qt6QuickDialogs2)
BuildRequires:	cmake(Qt6QuickDialogs2QuickImpl)
BuildRequires:	cmake(Qt6QuickDialogs2Utils)
BuildRequires:	cmake(Qt6QuickLayouts)
BuildRequires:	cmake(Qt6QuickTemplates2)
BuildRequires:	cmake(Qt6QuickTest)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	cmake(Qt6QuickTimeline)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6Quick3D)
BuildRequires:	cmake(Qt6Quick3DRuntimeRender)
BuildRequires:	cmake(Qt6Quick3DUtils)
BuildRequires:	qt6-qtdeclarative
BuildRequires:	cmake(Qt6ShaderTools) >= %{version}-0

BuildRequires:	qt6-cmake
BuildRequires:	pkgconfig(zlib)
BuildRequires:	cmake(OpenGL)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{qtmajor} 3D library

%global extra_files_Quick3DPhysics \
%dir %{_qtdir}/qml/QtQuick3D/Physics \
%{_qtdir}/qml/QtQuick3D/Physics/libqquick3dphysicsplugin.so \
%{_qtdir}/qml/QtQuick3D/Physics/plugins.qmltypes \
%{_qtdir}/qml/QtQuick3D/Physics/qmldir \
%{_qtdir}/bin/cooker

%global extra_devel_files_Quick3DPhysics \
%{_qtdir}/qml/QtQuick3D/Physics/designer \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6qquick3dphysicsplugin*.cmake \
%{_qtdir}/sbom/*

%global extra_files_Quick3DPhysicsHelpers \
%dir %{_qtdir}/qml/QtQuick3D/Physics/Helpers \
%{_qtdir}/qml/QtQuick3D/Physics/Helpers/libqtquick3dphysicshelpersplugin.so \
%{_qtdir}/qml/QtQuick3D/Physics/Helpers/plugins.qmltypes \
%{_qtdir}/qml/QtQuick3D/Physics/Helpers/qmldir

%global extra_devel_files_Quick3DPhysicsHelpers \
%{_qtdir}/lib/cmake/Qt6/FindWrapBundledPhysXConfigExtra.cmake \
%{_qtdir}/lib/cmake/Qt6BundledPhysX \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6qtquick3dphysicshelpersplugin*.cmake \
%{_qtdir}/lib/libQt6BundledPhysX.a

%qt6libs Quick3DPhysics Quick3DPhysicsHelpers

%package examples
Summary:	Example code for the Qt 6 3D module
Group:		Documentation

%description examples
Example code for the Qt 6 3D module

%prep
%autosetup -p1 -n qtquick3dphysics%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_MKSPECS_DIR:FILEPATH=%{_qtdir}/mkspecs \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall

%files examples
%{_qtdir}/examples
