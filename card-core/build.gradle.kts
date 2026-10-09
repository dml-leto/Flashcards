plugins {
    kotlin("jvm")
}

dependencies {
    api(project(":card-api"))
}

kotlin {
    jvmToolchain {
        languageVersion = JavaLanguageVersion.of(25)
        vendor = JvmVendorSpec.AMAZON
    }
}
