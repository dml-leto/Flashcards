plugins {
    kotlin("jvm")
}

dependencies {
    implementation(project(":card-core"))
}

kotlin {
    jvmToolchain {
        languageVersion = JavaLanguageVersion.of(25)
        vendor = JvmVendorSpec.AMAZON
    }
}
